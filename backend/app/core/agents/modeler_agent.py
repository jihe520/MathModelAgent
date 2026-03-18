from app.core.agents.agent import Agent
from app.core.llm.llm import LLM
from app.core.prompts import MODELER_PROMPT
from app.schemas.A2A import CoordinatorToModeler, ModelerToCoder
from app.utils.log_util import logger
import json
import re
from icecream import ic


def repair_json(json_str: str) -> dict | None:
    """Try to repair malformed JSON from LLM output."""
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
    def __init__(
        self,
        task_id: str,
        model: LLM,
        max_chat_turns: int = 30,
    ) -> None:
        super().__init__(task_id, model, max_chat_turns)
        self.system_prompt = MODELER_PROMPT

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

        max_parse_retries = 3
        for attempt in range(max_parse_retries):
            response = await self.model.chat(
                history=self.chat_history,
                agent_name=self.__class__.__name__,
            )

            json_str = response.choices[0].message.content
            if not json_str:
                raise ValueError("返回的 JSON 字符串为空，请检查输入内容。")

            questions_solution = repair_json(json_str)
            if questions_solution:
                ic(questions_solution)
                return ModelerToCoder(questions_solution=questions_solution)

            logger.warning(
                f"JSON 解析失败 (第{attempt + 1}次)，请求模型重新生成"
            )
            await self.append_chat_history(
                {"role": "assistant", "content": json_str}
            )
            await self.append_chat_history(
                {
                    "role": "user",
                    "content": "你返回的JSON格式有误，请严格按照JSON格式重新输出，注意字符串值内的双引号必须转义为\\\"，不要包含未转义的特殊字符。",
                }
            )

        raise ValueError(
            f"经过{max_parse_retries}次尝试仍无法解析JSON，请检查模型输出"
        )
