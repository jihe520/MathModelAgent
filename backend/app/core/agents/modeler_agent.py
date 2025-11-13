from app.core.agents.agent import Agent
from app.core.llm.llm import LLM
from app.core.prompts import MODELER_PROMPT
from app.schemas.A2A import CoordinatorToModeler, ModelerToCoder
from app.utils.log_util import logger
import json
from icecream import ic

# TODO: 提问工具tool


class ModelerAgent(Agent):  # 继承自Agent类
    def __init__(
        self,
        task_id: str,
        model: LLM,
        max_chat_turns: int = 30,  # 添加最大对话轮次限制
    ) -> None:
        super().__init__(task_id, model, max_chat_turns)
        self.system_prompt = MODELER_PROMPT

    def _extract_json_from_response(self, response: str) -> str:
        """从 LLM 响应中提取 JSON 内容"""
        # 如果响应已经是以 { 开头，直接返回
        if response.startswith('{'):
            return response
            
        # 查找第一个 { 和最后一个 }
        start_idx = response.find('{')
        end_idx = response.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
            extracted = response[start_idx:end_idx+1]
            logger.info(f"从响应中提取JSON: {extracted[:100]}...")
            return extracted
        else:
            # 如果没有找到完整的JSON结构，记录完整响应
            logger.error(f"LLM 响应不包含有效JSON格式，完整响应: {response}")
            # 返回空字符串，让后续逻辑使用默认方案
            return ""

    def _get_default_modeling_solution(self) -> str:
        """生成默认的建模方案，作为 LLM 响应失败时的后备"""
        return """{
  "eda": "进行数据探索性分析，包括描述性统计、相关性分析、数据分布可视化等，使用散点图、箱线图、热力图等图表展示数据特征",
  "ques1": "建立多元线性回归模型分析变量间关系，使用最小二乘法估计参数，通过F检验和t检验验证模型显著性，计算R²评估拟合优度",
  "ques2": "采用生存分析方法，使用Kaplan-Meier估计器分析达标时间分布，Log-rank检验比较组间差异，确定最佳检测时点",
  "ques3": "构建多变量Cox比例风险模型，分析多因素对达标时间的影响，计算风险比HR，使用机器学习方法处理非线性关系",
  "ques4": "建立逻辑回归分类模型进行异常判定，结合多个生物标记物，使用ROC曲线评估模型性能，确定最佳判定阈值",
  "sensitivity_analysis": "通过蒙特卡洛模拟分析参数不确定性对结果的影响，评估模型稳健性，分析关键参数的敏感性"
}"""

    async def run(self, coordinator_to_modeler: CoordinatorToModeler) -> ModelerToCoder:
        await self.append_chat_history(
            {"role": "system", "content": self.system_prompt}
        )
        await self.append_chat_history(
            {
                "role": "user",
                "content": json.dumps(coordinator_to_modeler.questions),
            }
        )

        response = await self.model.chat(
            history=self.chat_history,
            agent_name=self.__class__.__name__,
        )

        json_str = response.choices[0].message.content

        # 清理响应内容
        json_str = json_str.replace("```json", "").replace("```", "").strip()
        
        # 记录原始响应用于调试
        logger.debug(f"LLM 原始响应: {json_str[:200]}...")
        
        # 尝试提取JSON内容
        json_str = self._extract_json_from_response(json_str)

        if not json_str:
            logger.warning("LLM 返回空内容，使用默认建模方案")
            json_str = self._get_default_modeling_solution()
        
        try:
            questions_solution = json.loads(json_str)
            ic(questions_solution)
            return ModelerToCoder(questions_solution=questions_solution)
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失败，原始内容: {json_str[:200]}...")
            logger.warning("使用默认建模方案作为后备")
            
            # 后备方案：生成默认的建模方案
            default_solution = self._get_default_modeling_solution()
            try:
                questions_solution = json.loads(default_solution)
                logger.info("成功使用默认建模方案")
                return ModelerToCoder(questions_solution=questions_solution)
            except json.JSONDecodeError:
                raise ValueError(f"JSON 解析错误且默认方案也失败: {e}")
