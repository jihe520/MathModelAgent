"""工作流模块，编排多 Agent 协作完成数学建模任务。"""

from app.core.agents import WriterAgent, CoderAgent, CoordinatorAgent, ModelerAgent
from app.core.agents.agent import Agent
from app.schemas.request import Problem
from app.schemas.response import SystemMessage
from app.schemas.A2A import CoderToWriter, WriterResponse
from app.tools.openalex_scholar import OpenAlexScholar
from app.utils.log_util import logger
from app.utils.common_utils import create_work_dir, get_config_template
from app.models.user_output import UserOutput
from app.config.setting import settings
from app.tools.interpreter_factory import create_interpreter
from app.services.redis_manager import redis_manager
from app.tools.notebook_serializer import NotebookSerializer
from app.core.flows import Flows
from app.core.llm.llm import LLM
from app.core.llm.llm_factory import LLMFactory
from app.tools.base_interpreter import BaseCodeInterpreter
from app.core.evaluator import Evaluator
from app.core.functions import coder_tools, search_web_tool, search_knowledge_tool
from app.tools.tool_registry import tool_registry
from app.tools.web_searcher import WebSearcher
from app.tools.knowledge_retriever import knowledge_retriever
from app.services.checkpoint_manager import checkpoint_manager


# CoderToWriter 中表示任务失败的前缀
_CODER_FAILURE_PREFIX = "任务失败"


def _is_coder_failed(response: CoderToWriter) -> bool:
    """判断 CoderToWriter 响应是否表示任务失败。

    Args:
        response: 代码手的响应。

    Returns:
        True 如果响应内容以失败前缀开头。
    """
    return bool(
        response.code_response
        and response.code_response.startswith(_CODER_FAILURE_PREFIX)
    )


class WorkFlow:
    """工作流基类。"""

    def __init__(self):
        pass

    def execute(self) -> None:
        """执行工作流。"""
        # RichPrinter.workflow_start()
        # RichPrinter.workflow_end()
        pass


class MathModelWorkFlow(WorkFlow):
    """数学建模工作流，协调协调者、建模手、代码手和写作手完成完整建模任务。"""

    task_id: str  #
    work_dir: str  # worklow work dir
    ques_count: int = 0  # 问题数量
    questions: dict[str, str | int] = {}  # 问题

    async def _run_with_handoff(
        self,
        agent: Agent,
        method_name: str,
        args: tuple,
        agent_label: str,
        fallback_llm: LLM | None,
        agent_cls: type,
        agent_init_kwargs: dict | None = None,
    ):
        """通用 Hand Off 包装器：主 Agent 失败时新建 Fallback Agent 重试。

        Args:
            agent: 主 Agent 实例。
            method_name: 要调用的方法名（如 "run"）。
            args: 方法参数元组。
            agent_label: 用于日志和消息的 Agent 标签。
            fallback_llm: Fallback LLM 实例，None 表示无 fallback。
            agent_cls: Agent 类，用于创建 fallback 实例。
            agent_init_kwargs: 创建 fallback Agent 时的额外关键字参数。

        Returns:
            方法调用的返回值。
        """
        try:
            method = getattr(agent, method_name)
            return await method(*args)
        except Exception as e:
            logger.error(f"{agent_label} 主 LLM 执行失败: {e}")
            if fallback_llm:
                await redis_manager.publish_message(
                    self.task_id,
                    SystemMessage(
                        content=f"{agent_label}主模型失败({type(e).__name__})，正在切换备用模型...",
                        type="warning",
                    ),
                )
                # 新建 Agent 实例，避免脏 chat_history
                init_kwargs = agent_init_kwargs or {}
                fallback_agent = agent_cls(self.task_id, fallback_llm, **init_kwargs)
                try:
                    method = getattr(fallback_agent, method_name)
                    return await method(*args)
                except Exception as fallback_e:
                    logger.error(f"{agent_label} Fallback 也失败: {fallback_e}")
                    raise fallback_e
            else:
                raise e

    async def _run_coder_with_handoff(
        self,
        coder_agent: CoderAgent,
        prompt: str,
        subtask_title: str,
        fallback_llm: LLM | None,
        code_interpreter: BaseCodeInterpreter,
        work_dir: str,
    ) -> CoderToWriter:
        """Coder 专用 Hand Off：主 Agent 返回失败响应或抛异常时切换 Fallback。

        Args:
            coder_agent: 主 CoderAgent 实例。
            prompt: 子任务提示。
            subtask_title: 子任务标题。
            fallback_llm: Fallback LLM 实例。
            code_interpreter: 代码解释器。
            work_dir: 工作目录。

        Returns:
            CoderToWriter 响应。
        """
        try:
            response = await coder_agent.run(prompt=prompt, subtask_title=subtask_title)
            if _is_coder_failed(response) and fallback_llm:
                # 主 Agent 返回失败响应，尝试 Fallback
                logger.warning("CoderAgent 主 LLM 返回失败响应，尝试 Fallback")
                await redis_manager.publish_message(
                    self.task_id,
                    SystemMessage(
                        content="代码手主模型失败，正在切换备用模型...",
                        type="warning",
                    ),
                )
                fallback_agent = CoderAgent(
                    task_id=self.task_id,
                    model=fallback_llm,
                    work_dir=work_dir,
                    max_retries=settings.MAX_RETRIES,
                    code_interpreter=code_interpreter,
                )
                return await fallback_agent.run(
                    prompt=prompt, subtask_title=subtask_title
                )
            return response
        except Exception as e:
            logger.error(f"CoderAgent 主 LLM 执行异常: {e}")
            if fallback_llm:
                await redis_manager.publish_message(
                    self.task_id,
                    SystemMessage(
                        content=f"代码手主模型异常({type(e).__name__})，正在切换备用模型...",
                        type="warning",
                    ),
                )
                fallback_agent = CoderAgent(
                    task_id=self.task_id,
                    model=fallback_llm,
                    work_dir=work_dir,
                    max_retries=settings.MAX_RETRIES,
                    code_interpreter=code_interpreter,
                )
                try:
                    return await fallback_agent.run(
                        prompt=prompt, subtask_title=subtask_title
                    )
                except Exception as fallback_e:
                    logger.error(f"CoderAgent Fallback 也失败: {fallback_e}")
                    raise fallback_e
            else:
                raise e

    async def _run_writer_with_feedback(
        self,
        writer_agent: WriterAgent,
        prompt: str,
        sub_title: str,
        evaluator: Evaluator | None,
        fallback_llm: LLM | None,
        agent_init_kwargs: dict,
    ) -> WriterResponse:
        """写作手 Feedback Rerun：评估不通过时注入反馈重跑。

        通过拼接反馈到 prompt 末尾实现，利用已有的 run(prompt) 接口。

        Args:
            writer_agent: 写作手 Agent 实例。
            prompt: 原始写作提示。
            sub_title: 子任务标题。
            evaluator: 评估器实例，None 表示无评估。
            fallback_llm: Fallback LLM 实例。
            agent_init_kwargs: 创建 fallback Agent 时的额外参数。

        Returns:
            WriterResponse 响应。
        """
        current_prompt = prompt
        last_response = None

        for feedback_round in range(settings.MAX_FEEDBACK_ROUNDS + 1):
            response = await self._run_with_handoff(
                agent=writer_agent,
                method_name="run",
                args=(current_prompt,),
                agent_label="写作手",
                fallback_llm=fallback_llm,
                agent_cls=WriterAgent,
                agent_init_kwargs=agent_init_kwargs,
            )
            last_response = response

            # 最后一轮或无评估器，不再重跑
            if not evaluator or feedback_round == settings.MAX_FEEDBACK_ROUNDS:
                break

            eval_result = await evaluator.evaluate(
                task_description=current_prompt,
                agent_output=str(response.response_content)[:2000],
            )
            logger.info(
                f"[Feedback] 写作手 {sub_title} 第{feedback_round + 1}轮评估: "
                f"score={eval_result.score:.2f}, passed={eval_result.passed}"
            )

            if eval_result.passed or eval_result.score >= settings.EVALUATION_THRESHOLD:
                break

            # 注入反馈到 prompt 末尾
            current_prompt = f"{prompt}\n\n【评估反馈（第{feedback_round + 1}轮）】\n{eval_result.feedback}"
            await redis_manager.publish_message(
                self.task_id,
                SystemMessage(
                    content=f"写作手 {sub_title} 评估未通过(score={eval_result.score:.2f})，注入反馈重跑...",
                    type="warning",
                ),
            )
            # 新建 Agent 实例以获得干净状态
            writer_agent = WriterAgent(
                self.task_id, writer_agent.model, **agent_init_kwargs
            )

        return last_response  # type: ignore[return-value]

    async def _run_coder_with_feedback(
        self,
        coder_agent: CoderAgent,
        prompt: str,
        subtask_title: str,
        evaluator: Evaluator | None,
        fallback_llm: LLM | None,
        code_interpreter: BaseCodeInterpreter,
        work_dir: str,
    ) -> CoderToWriter:
        """代码手 Feedback Rerun：评估不通过时注入反馈重跑。

        Args:
            coder_agent: 代码手 Agent 实例。
            prompt: 原始任务提示。
            subtask_title: 子任务标题。
            evaluator: 评估器实例。
            fallback_llm: Fallback LLM 实例。
            code_interpreter: 代码解释器。
            work_dir: 工作目录。

        Returns:
            CoderToWriter 响应。
        """
        current_prompt = prompt
        last_response = None

        for feedback_round in range(settings.MAX_FEEDBACK_ROUNDS + 1):
            response = await self._run_coder_with_handoff(
                coder_agent=coder_agent,
                prompt=current_prompt,
                subtask_title=subtask_title,
                fallback_llm=fallback_llm,
                code_interpreter=code_interpreter,
                work_dir=work_dir,
            )
            last_response = response

            if not evaluator or feedback_round == settings.MAX_FEEDBACK_ROUNDS:
                break

            if _is_coder_failed(response):
                break

            eval_result = await evaluator.evaluate(
                task_description=current_prompt,
                agent_output=response.code_response or "",
            )
            logger.info(
                f"[Feedback] 代码手 {subtask_title} 第{feedback_round + 1}轮评估: "
                f"score={eval_result.score:.2f}, passed={eval_result.passed}"
            )

            if eval_result.passed or eval_result.score >= settings.EVALUATION_THRESHOLD:
                break

            current_prompt = f"{prompt}\n\n【评估反馈（第{feedback_round + 1}轮）】\n{eval_result.feedback}"
            await redis_manager.publish_message(
                self.task_id,
                SystemMessage(
                    content=f"代码手 {subtask_title} 评估未通过(score={eval_result.score:.2f})，注入反馈重跑...",
                    type="warning",
                ),
            )
            coder_agent = CoderAgent(
                task_id=self.task_id,
                model=coder_agent.model,
                work_dir=work_dir,
                max_retries=settings.MAX_RETRIES,
                code_interpreter=code_interpreter,
            )

        return last_response  # type: ignore[return-value]

    async def _handle_checkpoint(
        self,
        checkpoint_id: str,
        prompt: dict,
    ) -> dict:
        """处理 HIL 检查点，等待用户决策并返回。

        Args:
            checkpoint_id: 检查点 ID。
            prompt: 审批提示内容。

        Returns:
            用户决策字典，HIL 未启用时返回 {"action": "confirm"}。
        """
        if not settings.HIL_ENABLED:
            return {"action": "confirm"}

        checkpoints = settings.HIL_CHECKPOINTS
        # code_review 默认关闭，需显式开启
        if checkpoint_id.startswith("code_review") and not checkpoints.get(
            "code_review", False
        ):
            return {"action": "confirm"}
        if not checkpoints.get(checkpoint_id, True):
            return {"action": "confirm"}

        decision = await checkpoint_manager.wait_for_decision(
            task_id=self.task_id,
            checkpoint_id=checkpoint_id,
            prompt=prompt,
            timeout=settings.HIL_TIMEOUT,
        )
        return decision

    async def execute(self, problem: Problem):  # type: ignore[reportIncompatibleMethodOverride]
        """执行数学建模工作流。

        Args:
            problem: 包含题目信息、模板配置等的 Problem 对象。
        """
        self.task_id = problem.task_id
        self.work_dir = create_work_dir(self.task_id)

        llm_factory = LLMFactory(self.task_id)
        coordinator_llm, modeler_llm, coder_llm, writer_llm = llm_factory.get_all_llms()
        fallback_llms = llm_factory.get_fallback_llms()

        # 评估器（Shadow Mode：只记录不触发重跑）
        evaluator_llm = llm_factory.get_evaluator_llm()
        evaluator = Evaluator(evaluator_llm) if evaluator_llm else None

        coordinator_agent = CoordinatorAgent(self.task_id, coordinator_llm)

        # ---- Web Search 初始化 ----
        search_evidence: list = []
        active_coder_tools = list(coder_tools)  # 复制默认工具列表
        modeler_tools: list[dict] | None = None

        if settings.SEARCH_ENABLED and settings.TAVILY_API_KEY:
            web_searcher = WebSearcher(modeler_llm)

            async def _search_handler(arguments: dict, task_id: str) -> str:
                """search_web 工具 handler，同时收集 evidence。"""
                query = arguments.get("query", "")
                data_type = arguments.get("data_type", "general")
                max_results = arguments.get("max_results", 5)

                evidence_list = await web_searcher.search(query, data_type, max_results)
                search_evidence.extend(evidence_list)

                if not evidence_list:
                    return "未搜索到相关数据"

                result_parts = []
                for i, ev in enumerate(evidence_list, 1):
                    part = f"[数据 {i}] {ev.content}"
                    if ev.unit:
                        part += f" (单位: {ev.unit})"
                    if ev.time_range:
                        part += f" (时间: {ev.time_range})"
                    if ev.region:
                        part += f" (地域: {ev.region})"
                    if ev.source_url:
                        part += f"\n  来源: {ev.source_url}"
                    if ev.original_excerpt:
                        part += f"\n  原文: {ev.original_excerpt[:200]}"
                    result_parts.append(part)

                return "\n\n".join(result_parts)

            tool_registry.register("search_web", _search_handler, search_web_tool)
            active_coder_tools.append(search_web_tool)
            modeler_tools = [search_web_tool]

        # ---- RAG 知识库初始化 ----
        if settings.RAG_ENABLED:
            active_coder_tools.append(search_knowledge_tool)
            if modeler_tools is not None:
                modeler_tools.append(search_knowledge_tool)

            async def _knowledge_handler(arguments: dict, task_id: str) -> str:
                """search_knowledge 工具 handler。"""
                query = arguments.get("query", "")
                scope = arguments.get("scope", "method")
                method_name = arguments.get("method_name", "") or None

                # 根据 scope 映射 source_type
                scope_map = {
                    "method": "textbook,paper",
                    "code": "code",
                    "paper": "paper,problem",
                }
                source_type = scope_map.get(scope, "textbook")

                evidence_list = await knowledge_retriever.retrieve(
                    query=query, source_type=source_type, method_name=method_name
                )
                if not evidence_list:
                    return "知识库中未找到相关内容"

                result_parts = []
                for i, ke in enumerate(evidence_list, 1):
                    part = f"[知识 {i}] {ke.content[:400]}"
                    if ke.method_name:
                        part += f" (方法: {ke.method_name})"
                    if ke.source_title:
                        part += f" (来源: {ke.source_title})"
                    result_parts.append(part)

                return "\n\n".join(result_parts)

            tool_registry.register(
                "search_knowledge", _knowledge_handler, search_knowledge_tool
            )

        await redis_manager.publish_message(
            self.task_id,
            SystemMessage(content="识别用户意图和拆解问题ing..."),
        )

        # ---- Coordinator: 主 LLM → Fallback Hand Off ----
        coordinator_response = await self._run_with_handoff(
            agent=coordinator_agent,
            method_name="run",
            args=(problem.ques_all,),
            agent_label="协调者",
            fallback_llm=fallback_llms.get("coordinator"),
            agent_cls=CoordinatorAgent,
        )
        self.questions = coordinator_response.questions
        self.ques_count = coordinator_response.ques_count

        # ---- HIL Checkpoint: problem_split ----
        hil_decision = await self._handle_checkpoint(
            "problem_split",
            {"step": "problem_split", "questions": coordinator_response.questions},
        )
        if hil_decision.get("action") == "abort":
            await redis_manager.publish_message(
                self.task_id, SystemMessage(content="用户中止任务", type="error")
            )
            return
        if hil_decision.get("action") == "edit":
            # 用用户修改后的问题继续
            coordinator_response.questions = hil_decision.get(
                "content", coordinator_response.questions
            )
            self.questions = coordinator_response.questions

        await redis_manager.publish_message(
            self.task_id,
            SystemMessage(content="识别用户意图和拆解问题完成,任务转交给建模手"),
        )

        await redis_manager.publish_message(
            self.task_id,
            SystemMessage(content="建模手开始建模ing..."),
        )

        # ---- RAG: 为建模手检索知识 ----
        modeler_knowledge_text = ""
        if settings.RAG_ENABLED:
            # 根据问题描述检索建模方法知识
            query_text = " ".join(
                str(v) for v in self.questions.values() if isinstance(v, str)
            )[:500]
            modeler_knowledge = await knowledge_retriever.retrieve(
                query=query_text, source_type="textbook,paper"
            )
            if modeler_knowledge:
                knowledge_lines = []
                for ke in modeler_knowledge:
                    line = f"- {ke.content[:300]}"
                    if ke.method_name:
                        line += f" (方法: {ke.method_name})"
                    if ke.source_title:
                        line += f" (来源: {ke.source_title})"
                    knowledge_lines.append(line)
                modeler_knowledge_text = (
                    "\n【知识库参考】\n" + "\n".join(knowledge_lines) + "\n"
                )

        # ---- Modeler: 主 LLM → Fallback Hand Off ----
        modeler_agent = ModelerAgent(self.task_id, modeler_llm)
        if modeler_tools:
            # 支持工具调用的建模手（单次 tool call 模式）
            try:
                # 注入知识库参考到 questions
                if modeler_knowledge_text:
                    coordinator_response.questions["_knowledge_reference"] = (
                        modeler_knowledge_text
                    )
                modeler_response = await modeler_agent.run_with_tools(
                    coordinator_response, tools=modeler_tools
                )
            except Exception as e:
                logger.error(f"建模手主 LLM 执行失败: {e}")
                fallback_llm = fallback_llms.get("modeler")
                if fallback_llm:
                    await redis_manager.publish_message(
                        self.task_id,
                        SystemMessage(
                            content=f"建模手主模型失败({type(e).__name__})，正在切换备用模型...",
                            type="warning",
                        ),
                    )
                    fallback_agent = ModelerAgent(self.task_id, fallback_llm)
                    modeler_response = await fallback_agent.run_with_tools(
                        coordinator_response, tools=modeler_tools
                    )
                else:
                    raise
        else:
            modeler_response = await self._run_with_handoff(
                agent=modeler_agent,
                method_name="run",
                args=(coordinator_response,),
                agent_label="建模手",
                fallback_llm=fallback_llms.get("modeler"),
                agent_cls=ModelerAgent,
            )

        user_output = UserOutput(work_dir=self.work_dir, ques_count=self.ques_count)

        # ---- HIL Checkpoint: model_selection ----
        hil_decision = await self._handle_checkpoint(
            "model_selection",
            {
                "step": "model_selection",
                "solutions": modeler_response.questions_solution,
            },
        )
        if hil_decision.get("action") == "abort":
            await redis_manager.publish_message(
                self.task_id, SystemMessage(content="用户中止任务", type="error")
            )
            return
        if hil_decision.get("action") == "edit":
            modeler_response.questions_solution = hil_decision.get(
                "content", modeler_response.questions_solution
            )
        if hil_decision.get("action") == "regenerate":
            modeler_agent = ModelerAgent(self.task_id, modeler_llm)
            if modeler_tools:
                modeler_response = await modeler_agent.run_with_tools(
                    coordinator_response, tools=modeler_tools
                )
            else:
                modeler_response = await self._run_with_handoff(
                    agent=modeler_agent,
                    method_name="run",
                    args=(coordinator_response,),
                    agent_label="建模手(重新生成)",
                    fallback_llm=fallback_llms.get("modeler"),
                    agent_cls=ModelerAgent,
                )

        await redis_manager.publish_message(
            self.task_id,
            SystemMessage(content="正在创建代码沙盒环境"),
        )

        notebook_serializer = NotebookSerializer(work_dir=self.work_dir)
        code_interpreter = await create_interpreter(
            kind="local",
            task_id=self.task_id,
            work_dir=self.work_dir,
            notebook_serializer=notebook_serializer,
            timeout=3000,
        )

        assert settings.OPENALEX_EMAIL is not None, "OPENALEX_EMAIL 未配置"
        assert settings.OPENALEX_API_KEY is not None, "OPENALEX_API_KEY 未配置"
        scholar = OpenAlexScholar(
            task_id=self.task_id,
            email=settings.OPENALEX_EMAIL,
            api_key=settings.OPENALEX_API_KEY,
        )

        await redis_manager.publish_message(
            self.task_id,
            SystemMessage(content="创建完成"),
        )

        await redis_manager.publish_message(
            self.task_id,
            SystemMessage(content="初始化代码手"),
        )

        coder_agent = CoderAgent(
            task_id=problem.task_id,
            model=coder_llm,
            work_dir=self.work_dir,
            max_chat_turns=settings.MAX_CHAT_TURNS,
            max_retries=settings.MAX_RETRIES,
            code_interpreter=code_interpreter,
        )
        # 更新 coder 的可用工具列表（包含 search_web 等动态注册的工具）
        coder_agent.available_tools = active_coder_tools

        writer_agent = WriterAgent(
            task_id=problem.task_id,
            model=writer_llm,
            comp_template=problem.comp_template,
            format_output=problem.format_output,
            scholar=scholar,
        )

        flows = Flows(self.questions)

        ################################################ solution steps

        # ---- RAG: 为代码手检索代码模板知识 ----
        coder_knowledge = None
        if settings.RAG_ENABLED:
            query_text = " ".join(
                str(v) for v in self.questions.values() if isinstance(v, str)
            )[:500]
            coder_knowledge = await knowledge_retriever.retrieve(
                query=query_text, source_type="code"
            )

        solution_flows = flows.get_solution_flows(
            self.questions,
            modeler_response,
            search_evidence=search_evidence or None,
            coder_knowledge=coder_knowledge,
        )
        config_template = get_config_template(problem.comp_template)

        writer_agent_init_kwargs = {
            "comp_template": problem.comp_template,
            "format_output": problem.format_output,
            "scholar": scholar,
        }

        for key, value in solution_flows.items():
            await redis_manager.publish_message(
                self.task_id,
                SystemMessage(content=f"代码手开始求解{key}"),
            )

            # ---- Coder: Feedback Rerun + Hand Off ----
            coder_response = await self._run_coder_with_feedback(
                coder_agent=coder_agent,
                prompt=value["coder_prompt"],
                subtask_title=key,
                evaluator=evaluator,
                fallback_llm=fallback_llms.get("coder"),
                code_interpreter=code_interpreter,
                work_dir=self.work_dir,
            )

            await redis_manager.publish_message(
                self.task_id,
                SystemMessage(content=f"代码手求解成功{key}", type="success"),
            )

            # ---- HIL Checkpoint: code_review_{key} ----
            hil_decision = await self._handle_checkpoint(
                f"code_review_{key}",
                {
                    "step": f"code_review_{key}",
                    "subtask": key,
                    "code_response": coder_response.code_response or "",
                },
            )
            if hil_decision.get("action") == "abort":
                await redis_manager.publish_message(
                    self.task_id, SystemMessage(content="用户中止任务", type="error")
                )
                return
            if hil_decision.get("action") == "regenerate":
                coder_response = await self._run_coder_with_feedback(
                    coder_agent=coder_agent,
                    prompt=value["coder_prompt"],
                    subtask_title=key,
                    evaluator=evaluator,
                    fallback_llm=fallback_llms.get("coder"),
                    code_interpreter=code_interpreter,
                    work_dir=self.work_dir,
                )

            writer_prompt = flows.get_writer_prompt(
                key,
                coder_response.code_response or "",
                code_interpreter,
                config_template,
            )

            await redis_manager.publish_message(
                self.task_id,
                SystemMessage(content=f"论文手开始写{key}部分"),
            )

            # ---- Writer: Feedback Rerun + Hand Off ----
            writer_response = await self._run_writer_with_feedback(
                writer_agent=writer_agent,
                prompt=writer_prompt,
                sub_title=key,
                evaluator=evaluator,
                fallback_llm=fallback_llms.get("writer"),
                agent_init_kwargs=writer_agent_init_kwargs,
            )

            await redis_manager.publish_message(
                self.task_id,
                SystemMessage(content=f"论文手完成{key}部分"),
            )

            user_output.set_res(key, writer_response)

        # 关闭沙盒

        await code_interpreter.cleanup()
        logger.info(user_output.get_res())

        ################################################ write steps

        # ---- RAG: 为写作手检索论文写作模板知识 ----
        writer_knowledge = None
        if settings.RAG_ENABLED:
            writer_knowledge = await knowledge_retriever.retrieve(
                query=str(problem.ques_all)[:500], source_type="paper,problem"
            )

        write_flows = flows.get_write_flows(
            user_output,
            config_template,
            problem.ques_all,
            writer_knowledge=writer_knowledge,
        )
        for key, value in write_flows.items():
            await redis_manager.publish_message(
                self.task_id,
                SystemMessage(content=f"论文手开始写{key}部分"),
            )

            writer_response = await self._run_writer_with_feedback(
                writer_agent=writer_agent,
                prompt=value,
                sub_title=key,
                evaluator=evaluator,
                fallback_llm=fallback_llms.get("writer"),
                agent_init_kwargs=writer_agent_init_kwargs,
            )

            user_output.set_res(key, writer_response)

        logger.info(user_output.get_res())

        # ---- HIL Checkpoint: paper_review ----
        hil_decision = await self._handle_checkpoint(
            "paper_review",
            {
                "step": "paper_review",
                "summary": user_output.get_res(),
            },
        )
        if hil_decision.get("action") == "abort":
            await redis_manager.publish_message(
                self.task_id, SystemMessage(content="用户中止任务", type="error")
            )
            return

        user_output.save_result()
