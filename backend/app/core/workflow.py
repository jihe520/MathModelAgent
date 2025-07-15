from app.core.agents import ModelerAgent, WriterAgent, CoderAgent
from app.core.llm import LLM, simple_chat
from app.models.model import CoderToWriter
from app.schemas.request import Problem
from app.schemas.response import SystemMessage
from app.utils.log_util import logger
from app.utils.common_utils import create_work_dir, get_config_template
from app.models.user_output import UserOutput
from app.config.setting import settings
from app.tools.interpreter_factory import create_interpreter
import json
from app.utils.redis_manager import redis_manager
from app.utils.notebook_serializer import NotebookSerializer
from app.tools.base_interpreter import BaseCodeInterpreter


class WorkFlow:
    def __init__(self):
        pass

    def execute(self) -> str:
        # RichPrinter.workflow_start()
        # RichPrinter.workflow_end()
        pass


class MathModelWorkFlow(WorkFlow):
    task_id: str  #
    work_dir: str  # worklow work dir
    ques_count: int = 0  # 问题数量
    questions: dict[str, str | int] = {}  # 问题

    async def execute(self, problem: Problem):
        self.task_id = problem.task_id
        self.work_dir = create_work_dir(self.task_id)

        # default choose deepseek model
        llm_model = LLM(
            api_key=settings.API_KEY,
            model=settings.MODEL,
            base_url=settings.BASE_URL,
            task_id=self.task_id,
        )

        await redis_manager.publish_message(
            self.task_id,
            SystemMessage(content="正在拆解问题问题"),
        )

        await self.format_questions(problem.ques_all, llm_model)

        user_output = UserOutput(work_dir=self.work_dir)

        notebook_serializer = NotebookSerializer(work_dir=self.work_dir)

        await redis_manager.publish_message(
            self.task_id,
            SystemMessage(content="正在创建代码沙盒环境"),
        )

        code_interpreter = await create_interpreter(
            kind="local",
            task_id=self.task_id,
            work_dir=self.work_dir,
            notebook_serializer=notebook_serializer,
            timeout=3000,
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
            model=llm_model,
            work_dir=self.work_dir,
            max_chat_turns=settings.MAX_CHAT_TURNS,
            max_retries=settings.MAX_RETRIES,
            code_interpreter=code_interpreter,
        )

        # TODO: 自定义 writer_agent mode llm
        writer_agent = WriterAgent(
            task_id=problem.task_id,
            model=llm_model,
            comp_template=problem.comp_template,
            format_output=problem.format_output,
        )

        modeler_agent = ModelerAgent(
            task_id=problem.task_id,
            model=llm_model,
        )

        ################################################ solution steps
        solution_steps = self.get_solution_steps()

        config_template = get_config_template(problem.comp_template)

        data_features_description = ""
        recommended_model = "linear_regression"  # Default model

        for key, value in solution_steps.items():
            if key == "eda":
                await redis_manager.publish_message(
                    self.task_id,
                    SystemMessage(content=f"代码手开始求解{key}"),
                )
                coder_response = await coder_agent.run(
                    prompt=value["coder_prompt"], subtask_title=key
                )
                data_features_description = coder_response  # Assume coder_response contains data features

            elif key.startswith("ques"):
                recommended_model = await modeler_agent.recommend_model(
                    user_prompt=self.questions[key],
                    data_features=data_features_description,
                )
                await redis_manager.publish_message(
                    self.task_id,
                    SystemMessage(content=f"推荐模型: {recommended_model}"),
                )

                value["coder_prompt"] = f"{value['coder_prompt']}\n请使用 {recommended_model} 模型."

                await redis_manager.publish_message(
                    self.task_id,
                    SystemMessage(content=f"代码手开始求解{key}"),
                )
                coder_response = await coder_agent.run(
                    prompt=value["coder_prompt"], subtask_title=key
                )
            else:
                await redis_manager.publish_message(
                    self.task_id,
                    SystemMessage(content=f"代码手开始求解{key}"),
                )

                coder_response = await coder_agent.run(
                    prompt=value["coder_prompt"], subtask_title=key
                )

            await redis_manager.publish_message(
                self.task_id,
                SystemMessage(content=f"代码手求解成功{key}", type="success"),
            )

            # TODO: 是否可以不需要coder_response
            writer_prompt = self.get_writer_prompt(
                key, coder_response, code_interpreter, config_template
            )

            await redis_manager.publish_message(
                self.task_id,
                SystemMessage(content=f"论文手开始写{key}部分"),
            )

            ## TODO: 图片引用错误
            writer_response = await writer_agent.run(
                writer_prompt,
                available_images=await code_interpreter.get_created_images(key),
                sub_title=key,
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

        flows = self.get_write_flows(user_output, config_template, problem.ques_all)
        for key, value in flows.items():
            await redis_manager.publish_message(
                self.task_id,
                SystemMessage(content=f"论文手开始写{key}部分"),
            )

            # TODO: writer_agent 是否不需要初始化
            writer_agent = WriterAgent(
                task_id=problem.task_id,
                model=llm_model,
                comp_template=problem.comp_template,
                format_output=problem.format_output,
            )
            writer_response = await writer_agent.run(prompt=value, sub_title=key)
            user_output.set_res(key, writer_response)

        logger.info(user_output.get_res())

        user_output.save_result(ques_count=self.ques_count)

    async def format_questions(self, ques_all: str, model: LLM) -> None:
        """用户输入问题 使用LLM 格式化 questions"""
        # TODO:  "note": <补充说明,如果没有补充说明，请填 null>,
        from app.core.prompts import FORMAT_QUESTIONS_PROMPT

        history = [
            {
                "role": "system",
                "content": FORMAT_QUESTIONS_PROMPT,
            },
            {"role": "user", "content": ques_all},
        ]
        json_str = await simple_chat(model, history)
        json_str = json_str.replace("```json", "").replace("```", "").strip()

        if not json_str:
            raise ValueError("返回的 JSON 字符串为空，请检查输入内容。")

        try:
            self.questions = json.loads(json_str)
            self.ques_count = self.questions["ques_count"]
            logger.info(f"questions:{self.questions}")
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 解析错误: {e}")

    def get_solution_steps(self):
        questions_quesx = {
            key: value
            for key, value in self.questions.items()
            if key.startswith("ques") and key != "ques_count"
        }
        ques_flow = {
            key: {
                "coder_prompt": f"""
                        完成如下问题{value}
                    """,
            }
            for key, value in questions_quesx.items()
        }
        flows = {
            "eda": {
                # TODO ： 获取当前路径下的所有数据集
                "coder_prompt": """
                        对当前目录下数据进行EDA分析(数据清洗,可视化),清洗后的数据保存当前目录下,**不需要复杂的模型**
                    """,
            },
            **ques_flow,
            "sensitivity_analysis": {
                "coder_prompt": """
                        根据上面建立的模型，选择一个模型，完成敏感性分析
                    """,
            },
        }
        return flows

    def get_writer_prompt(
        self,
        key: str,
        coder_response: str,
        code_interpreter: BaseCodeInterpreter,
        config_template: dict,
    ) -> str:
        """根据不同的key生成对应的writer_prompt

        Args:
            key: 任务类型
            coder_response: 代码执行结果

        Returns:
            str: 生成的writer_prompt
        """
        code_output = code_interpreter.get_code_output(key)

        # TODO: 结果{coder_response} 是否需要
        # TODO: 将当前产生的文件，路径发送给 writer_agent
        questions_quesx_keys = self.get_questions_quesx_keys()
        # TODO： 小标题编号
        # 题号最多6题
        bgc = self.questions["background"]
        quesx_writer_prompt = {
            key: f"""
                    问题背景{bgc},不需要编写代码,代码手得到的结果{coder_response},{code_output},按照如下模板撰写：{config_template[key]}
                """
            for key in questions_quesx_keys
        }

        writer_prompt = {
            "eda": f"""
                    问题背景{bgc},不需要编写代码,代码手得到的结果{coder_response},{code_output},按照如下模板撰写：{config_template["eda"]}
                """,
            **quesx_writer_prompt,
            "sensitivity_analysis": f"""
                    问题背景{bgc},不需要编写代码,代码手得到的结果{coder_response},{code_output},按照如下模板撰写：{config_template["sensitivity_analysis"]}
                """,
        }

        if key in writer_prompt:
            return writer_prompt[key]
        else:
            raise ValueError(f"未知的任务类型: {key}")

    def get_questions_quesx_keys(self) -> list[str]:
        """获取问题1,2...的键"""
        return list(self.get_questions_quesx().keys())

    def get_questions_quesx(self) -> dict[str, str]:
        """获取问题1,2,3...的键值对"""
        # 获取所有以 "ques" 开头的键值对
        questions_quesx = {
            key: value
            for key, value in self.questions.items()
            if key.startswith("ques") and key != "ques_count"
        }
        return questions_quesx

    def get_write_flows(
        self, user_output: UserOutput, config_template: dict, bg_ques_all: str
    ):
        model_build_solve = user_output.get_model_build_solve()
        flows = {
            "firstPage": f"""问题背景{bg_ques_all},不需要编写代码,根据模型的求解的信息{model_build_solve}，按照如下模板撰写：{config_template["firstPage"]}，撰写标题，摘要，关键词""",
            "RepeatQues": f"""问题背景{bg_ques_all},不需要编写代码,根据模型的求解的信息{model_build_solve}，按照如下模板撰写：{config_template["RepeatQues"]}，撰写问题重述""",
            "analysisQues": f"""问题背景{bg_ques_all},不需要编写代码,根据模型的求解的信息{model_build_solve}，按照如下模板撰写：{config_template["analysisQues"]}，撰写问题分析""",
            "modelAssumption": f"""问题背景{bg_ques_all},不需要编写代码,根据模型的求解的信息{model_build_solve}，按照如下模板撰写：{config_template["modelAssumption"]}，撰写模型假设""",
            "symbol": f"""不需要编写代码,根据模型的求解的信息{model_build_solve}，按照如下模板撰写：{config_template["symbol"]}，撰写符号说明部分""",
            "judge": f"""不需要编写代码,根据模型的求解的信息{model_build_solve}，按照如下模板撰写：{config_template["judge"]}，撰写模型的评价部分""",
            # TODO: 修改参考文献插入方式
            "reference": f"""不需要编写代码,根据模型的求解的信息{model_build_solve}，可以生成参考文献,按照如下模板撰写：{config_template["reference"]}，撰写参考文献""",
        }
        return flows
