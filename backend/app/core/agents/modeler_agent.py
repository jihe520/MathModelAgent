"""建模手 Agent 模块，负责分析问题并制定数学建模方案。"""

from app.core.agents.agent import Agent
from app.core.llm.llm import LLM
from app.core.prompts import MODELER_PROMPT
from app.schemas.A2A import CoordinatorToModeler, ModelerToCoder
from app.utils.log_util import logger
import json
import re
from icecream import ic  # type: ignore[import-unresolved]


def repair_json(json_str: str) -> dict | None:
    """尝试修复 LLM 输出的格式错误的 JSON。

    Args:
        json_str: 可能包含格式错误的 JSON 字符串。

    Returns:
        修复后的字典，无法修复时返回 None。
    """
    json_str = json_str.replace("```json", "").replace("```", "").strip()

    # Try direct parse first
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        pass

    # Fix unescaped newlines and quotes inside string values
    try:
        fixed = re.sub(
            r'(?<=: ")(.*?)(?=",\s*\n\s*"|"\s*\n\s*})',
            lambda m: m.group(0).replace('"', '\\"'),
            json_str,
            flags=re.DOTALL,
        )
        return json.loads(fixed)
    except (json.JSONDecodeError, re.error):
        pass

    # Extract key-value pairs with regex as last resort
    try:
        pattern = r'"(\w+)"\s*:\s*"((?:[^"\\]|\\.|"(?!,\s*\n)|"(?!\s*\n\s*}))*)"'
        matches = re.findall(pattern, json_str, re.DOTALL)
        if matches:
            return {k: v.replace('\\"', '"') for k, v in matches}
    except re.error:
        pass

    return None


class ModelerAgent(Agent):
    """建模手 Agent，分析问题类型并制定建模方案、求解方法和可视化策略。"""
    def __init__(
        self,
        task_id: str,
        model: LLM,
        context_window: int = 128000,
    ) -> None:
        super().__init__(task_id, model, context_window)
        self.system_prompt = MODELER_PROMPT

    async def run(self, coordinator_to_modeler: CoordinatorToModeler) -> ModelerToCoder:  # type: ignore[reportIncompatibleMethodOverride]
        """根据协调者拆解的问题生成建模方案。

        Args:
            coordinator_to_modeler: 协调者传递的结构化问题信息。

        Returns:
            ModelerToCoder 对象，包含各问题的建模解决方案。
        """
        await self.append_chat_history(
            {"role": "system", "content": self.system_prompt}
        )
        await self.append_chat_history(
            {
                "role": "user",
                "content": json.dumps(coordinator_to_modeler.questions),
            }
        )

        attempt = 0
        while True:
            response = await self.model.chat(
                history=self.chat_history,
                agent_name=self.__class__.__name__,
            )

            json_str = response.content
            if not json_str:
                raise ValueError("返回的 JSON 字符串为空，请检查输入内容。")

            questions_solution = repair_json(json_str)
            if questions_solution:
                ic(questions_solution)
                return ModelerToCoder(questions_solution=questions_solution)

            attempt += 1
            logger.warning(
                f"JSON 解析失败 (第{attempt}次)，请求模型重新生成"
            )
            retry_msg: dict = {"role": "assistant", "content": json_str}
            if response.reasoning_content:
                retry_msg["reasoning_content"] = response.reasoning_content
            await self.append_chat_history(retry_msg)
            await self.append_chat_history(
                {
                    "role": "user",
                    "content": "你返回的JSON格式有误，请严格按照JSON格式重新输出，注意字符串值内的双引号必须转义为\\\"，不要包含未转义的特殊字符。",
                }
            )
