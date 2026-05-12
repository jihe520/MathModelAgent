"""工作流程定义模块，管理建模任务的求解和写作流程。"""

from app.models.user_output import UserOutput
from app.tools.base_interpreter import BaseCodeInterpreter
from app.core.agents.modeler_agent import ModelerToCoder
from app.schemas.evidence import DataEvidence, KnowledgeEvidence


class Flows:
    """管理数学建模任务的求解流程和写作流程。"""

    def __init__(self, questions: dict[str, str | int]):
        self.flows: dict[str, dict] = {}
        self.questions: dict[str, str | int] = questions

    def set_flows(self, ques_count: int):
        """根据问题数量设置流程节点。

        Args:
            ques_count: 问题数量。
        """
        ques_str = [f"ques{i}" for i in range(1, ques_count + 1)]
        seq = [
            "firstPage",
            "RepeatQues",
            "analysisQues",
            "modelAssumption",
            "symbol",
            "eda",
            *ques_str,
            "sensitivity_analysis",
            "judge",
        ]
        self.flows = {key: {} for key in seq}

    def get_solution_flows(
        self,
        questions: dict[str, str | int],
        modeler_response: ModelerToCoder,
        search_evidence: list[DataEvidence] | None = None,
        coder_knowledge: list[KnowledgeEvidence] | None = None,
    ):
        """生成求解阶段的流程配置。

        Args:
            questions: 包含各问题描述的字典。
            modeler_response: 建模手的响应，包含各问题的解决方案。
            search_evidence: Web 搜索到的数据证据列表，注入到 coder prompt 中。
            coder_knowledge: RAG 检索的代码模板知识，注入到 coder prompt 中。

        Returns:
            求解流程配置字典，键为任务名，值包含 coder_prompt 等信息。
        """
        questions_quesx = {
            key: value
            for key, value in questions.items()
            if key.startswith("ques") and key != "ques_count"
        }
        solutions = modeler_response.questions_solution

        # 构造搜索结果注入文本
        evidence_text = ""
        if search_evidence:
            evidence_lines = []
            for ev in search_evidence:
                line = f"- {ev.content}"
                if ev.unit:
                    line += f" (单位: {ev.unit})"
                if ev.time_range:
                    line += f" (时间: {ev.time_range})"
                if ev.region:
                    line += f" (地域: {ev.region})"
                if ev.source_url:
                    line += f" (来源: {ev.source_url})"
                evidence_lines.append(line)
            evidence_text = (
                "\n【搜索到的真实数据】\n" + "\n".join(evidence_lines) + "\n"
            )

        # 构造知识库参考注入文本
        knowledge_text = ""
        if coder_knowledge:
            knowledge_lines = []
            for ke in coder_knowledge:
                line = f"- {ke.content[:300]}"
                if ke.source_title:
                    line += f" (来源: {ke.source_title})"
                knowledge_lines.append(line)
            knowledge_text = "\n【代码模板参考】\n" + "\n".join(knowledge_lines) + "\n"

        ques_flow = {
            key: {
                "coder_prompt": f"""
                        参考建模手给出的解决方案{solutions.get(key, "")}
                        完成如下问题{value}
                        {evidence_text}{knowledge_text}
                    """,
            }
            for key, value in questions_quesx.items()
        }
        flows = {
            "eda": {
                "coder_prompt": f"""
                        参考建模手给出的解决方案{solutions.get("eda", "对数据进行探索性分析")}
                        对当前目录下数据进行EDA分析(数据清洗,可视化),清洗后的数据保存当前目录下,**不需要复杂的模型**
                        {evidence_text}{knowledge_text}
                    """,
            },
            **ques_flow,
            "sensitivity_analysis": {
                "coder_prompt": f"""
                        参考建模手给出的解决方案{solutions.get("sensitivity_analysis", "对模型进行灵敏度分析")}
                        完成敏感性分析
                        {evidence_text}{knowledge_text}
                    """,
            },
        }
        return flows

    def get_write_flows(
        self,
        user_output: UserOutput,
        config_template: dict,
        bg_ques_all: str,
        writer_knowledge: list[KnowledgeEvidence] | None = None,
    ):
        """生成写作阶段的流程配置。

        Args:
            user_output: 用户输出对象，包含已求解的结果。
            config_template: 论文模板配置。
            bg_ques_all: 问题背景和题目信息。
            writer_knowledge: RAG 检索的论文写作模板知识。

        Returns:
            写作流程配置字典，键为章节名，值为写作提示。
        """
        model_build_solve = user_output.get_model_build_solve()

        # 构造写作知识参考注入文本
        knowledge_text = ""
        if writer_knowledge:
            knowledge_lines = []
            for ke in writer_knowledge:
                line = f"- {ke.content[:300]}"
                if ke.source_title:
                    line += f" (来源: {ke.source_title})"
                knowledge_lines.append(line)
            knowledge_text = "\n【写作模板参考】\n" + "\n".join(knowledge_lines) + "\n"

        flows = {
            "firstPage": f"""问题背景{bg_ques_all},不需要编写代码,根据模型的求解的信息{model_build_solve}，按照如下模板撰写：{config_template["firstPage"]}，撰写标题，摘要，关键词{knowledge_text}""",
            "RepeatQues": f"""问题背景{bg_ques_all},不需要编写代码,根据模型的求解的信息{model_build_solve}，按照如下模板撰写：{config_template["RepeatQues"]}，撰写问题重述{knowledge_text}""",
            "analysisQues": f"""问题背景{bg_ques_all},不需要编写代码,根据模型的求解的信息{model_build_solve}，按照如下模板撰写：{config_template["analysisQues"]}，撰写问题分析{knowledge_text}""",
            "modelAssumption": f"""问题背景{bg_ques_all},不需要编写代码,根据模型的求解的信息{model_build_solve}，按照如下模板撰写：{config_template["modelAssumption"]}，撰写模型假设{knowledge_text}""",
            "symbol": f"""不需要编写代码,根据模型的求解的信息{model_build_solve}，按照如下模板撰写：{config_template["symbol"]}，撰写符号说明部分{knowledge_text}""",
            "judge": f"""不需要编写代码,根据模型的求解的信息{model_build_solve}，按照如下模板撰写：{config_template["judge"]}，撰写模型的评价部分{knowledge_text}""",
        }
        return flows

    def get_writer_prompt(
        self,
        key: str,
        coder_response: str,
        code_interpreter: BaseCodeInterpreter,
        config_template: dict,
        writer_knowledge: list[KnowledgeEvidence] | None = None,
    ) -> str:
        """根据不同的key生成对应的writer_prompt

        Args:
            key: 任务类型
            coder_response: 代码执行结果
            code_interpreter: 代码解释器
            config_template: 论文模板配置
            writer_knowledge: RAG 检索的论文写作模板知识

        Returns:
            str: 生成的writer_prompt
        """
        code_output = code_interpreter.get_code_output(key)

        # 构造写作知识参考注入文本
        knowledge_text = ""
        if writer_knowledge:
            knowledge_lines = []
            for ke in writer_knowledge:
                line = f"- {ke.content[:300]}"
                if ke.source_title:
                    line += f" (来源: {ke.source_title})"
                knowledge_lines.append(line)
            knowledge_text = "\n【写作模板参考】\n" + "\n".join(knowledge_lines) + "\n"

        questions_quesx_keys = self.get_questions_quesx_keys()
        bgc = self.questions["background"]
        quesx_writer_prompt = {
            key: f"""
                    问题背景{bgc},不需要编写代码,代码手得到的结果{coder_response},{code_output},按照如下模板撰写：{config_template[key]}
                    {knowledge_text}
                """
            for key in questions_quesx_keys
        }

        writer_prompt = {
            "eda": f"""
                    问题背景{bgc},不需要编写代码,代码手得到的结果{coder_response},{code_output},按照如下模板撰写：{config_template["eda"]}
                    {knowledge_text}
                """,
            **quesx_writer_prompt,
            "sensitivity_analysis": f"""
                    问题背景{bgc},不需要编写代码,代码手得到的结果{coder_response},{code_output},按照如下模板撰写：{config_template["sensitivity_analysis"]}
                    {knowledge_text}
                """,
        }

        if key in writer_prompt:
            return writer_prompt[key]
        else:
            raise ValueError(f"未知的任务类型: {key}")

    def get_questions_quesx_keys(self) -> list[str]:
        """获取问题1,2...的键"""
        return list(self.get_questions_quesx().keys())

    def get_questions_quesx(self) -> dict[str, str | int]:
        """获取问题1,2,3...的键值对"""
        # 获取所有以 "ques" 开头的键值对
        questions_quesx = {
            key: value
            for key, value in self.questions.items()
            if key.startswith("ques") and key != "ques_count"
        }
        return questions_quesx

    def get_seq(self, ques_count: int) -> dict[str, str]:
        """获取论文章节顺序。

        Args:
            ques_count: 问题数量。

        Returns:
            以章节名为键的有序字典。
        """
        ques_str = [f"ques{i}" for i in range(1, ques_count + 1)]
        seq = [
            "firstPage",
            "RepeatQues",
            "analysisQues",
            "modelAssumption",
            "symbol",
            "eda",
            *ques_str,
            "sensitivity_analysis",
            "judge",
        ]
        return {key: "" for key in seq}
