"""评估器模块，用于评估 Agent 输出质量（Shadow Mode）。"""

import json
from app.core.llm.llm import LLM, simple_chat
from app.schemas.A2A import EvaluationResult
from app.utils.log_util import logger


# 评估器 system prompt
EVALUATOR_SYSTEM_PROMPT = """你是一个数学建模任务评估器。你需要评估 Agent 的输出质量。

请以 JSON 格式返回评估结果，包含以下字段：
- passed: bool，是否通过评估
- score: float，0-1 之间的评分
- feedback: str，具体的改进建议（中文）
- should_handoff: bool，是否建议切换到备用模型
- reason: str，评估理由（中文）

评估标准：
1. 输出是否完整、格式是否正确
2. 内容是否合理、有逻辑
3. 是否满足任务要求

严格输出 JSON 格式，不要包含其他内容。"""


class Evaluator:
    """评估器，使用独立的便宜 LLM 对 Agent 输出做单次评估。

    Shadow Mode 下只记录评估结果，不触发重跑。
    评估失败时默认 passed=True，不阻塞主流程。
    """

    def __init__(self, model: LLM) -> None:
        """初始化评估器。

        Args:
            model: 评估用 LLM 实例（独立的便宜模型）。
        """
        self.model = model

    async def evaluate(self, task_description: str, agent_output: str) -> EvaluationResult:
        """评估 Agent 输出质量。

        Args:
            task_description: 任务描述（原始 prompt）。
            agent_output: Agent 的输出内容。

        Returns:
            EvaluationResult 评估结果，评估失败时返回 passed=True 的默认结果。
        """
        if not self.model.model or not self.model.api_key:
            logger.debug("评估器未配置，跳过评估")
            return EvaluationResult()

        user_prompt = (
            f"【任务描述】\n{task_description}\n\n"
            f"【Agent 输出】\n{agent_output}"
        )

        history = [
            {"role": "system", "content": EVALUATOR_SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ]

        try:
            content = await simple_chat(self.model, history)
            # 清理 JSON 字符串
            content = content.replace("```json", "").replace("```", "").strip()
            data = json.loads(content)
            return EvaluationResult(
                passed=data.get("passed", True),
                score=data.get("score", 1.0),
                feedback=data.get("feedback", ""),
                should_handoff=data.get("should_handoff", False),
                reason=data.get("reason", ""),
            )
        except Exception as e:
            logger.warning(f"评估器执行失败，默认通过: {e}")
            return EvaluationResult()
