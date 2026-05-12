"""建模手 Agent 模块，负责分析问题并制定数学建模方案。"""

from app.core.agents.agent import Agent
from app.core.llm.llm import LLM
from app.core.prompts import MODELER_PROMPT
from app.config.setting import settings
from app.schemas.A2A import CoordinatorToModeler, ModelerToCoder
from app.services.redis_manager import redis_manager
from app.schemas.response import SystemMessage
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
        max_chat_turns: int = 30,
        max_retries: int = settings.MAX_MODELER_RETRIES,
    ) -> None:
        super().__init__(task_id, model, max_chat_turns)
        self.system_prompt = MODELER_PROMPT
        self.max_retries = max_retries

    async def run(self, coordinator_to_modeler: CoordinatorToModeler) -> ModelerToCoder:  # type: ignore[reportIncompatibleMethodOverride]
        """根据协调者拆解的问题生成建模方案。

        Args:
            coordinator_to_modeler: 协调者传递的结构化问题信息。

        Returns:
            ModelerToCoder 对象，包含各问题的建模解决方案。

        Raises:
            ValueError: 超过最大重试次数仍无法解析 JSON 时抛出。
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

        for attempt in range(self.max_retries + 1):
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
                f"JSON 解析失败 (第{attempt + 1}/{self.max_retries + 1}次)，请求模型重新生成"
            )
            await self.append_chat_history({"role": "assistant", "content": json_str})
            await self.append_chat_history(
                {
                    "role": "user",
                    "content": '你返回的JSON格式有误，请严格按照JSON格式重新输出，注意字符串值内的双引号必须转义为\\"，不要包含未转义的特殊字符。',
                }
            )

        raise ValueError(
            f"ModelerAgent 超过最大重试次数({self.max_retries})，无法解析 JSON 响应"
        )

    async def run_with_tools(
        self,
        coordinator_to_modeler: CoordinatorToModeler,
        tools: list[dict] | None = None,
    ) -> ModelerToCoder:
        """支持工具调用的建模方案生成（单次 tool call 模式）。

        Args:
            coordinator_to_modeler: 协调者传递的结构化问题信息。
            tools: OpenAI function-calling 格式的工具列表。

        Returns:
            ModelerToCoder 对象，包含各问题的建模解决方案。

        Raises:
            ValueError: 超过最大重试次数仍无法解析 JSON 时抛出。
        """
        from app.tools.tool_registry import tool_registry

        await self.append_chat_history(
            {"role": "system", "content": self.system_prompt}
        )
        await self.append_chat_history(
            {
                "role": "user",
                "content": json.dumps(coordinator_to_modeler.questions),
            }
        )

        for attempt in range(self.max_retries + 1):
            response = await self.model.chat(
                history=self.chat_history,
                tools=tools,
                tool_choice="auto" if tools else None,
                agent_name=self.__class__.__name__,
            )

            msg = response.choices[0].message

            # 处理工具调用（单次，类似 WriterAgent）
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                tool_call = msg.tool_calls[0]
                tool_id = tool_call.id
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                logger.info(f"ModelerAgent 调用工具: {tool_name}")
                await redis_manager.publish_message(
                    self.task_id,
                    SystemMessage(content=f"建模手调用{tool_name}工具"),
                )

                await self.append_chat_history(msg.model_dump())

                try:
                    result = await tool_registry.dispatch(
                        tool_name, tool_args, self.task_id
                    )
                except ValueError as e:
                    result = f"工具调用失败: {e}"

                await self.append_chat_history(
                    {
                        "role": "tool",
                        "tool_call_id": tool_id,
                        "name": tool_name,
                        "content": result,
                    }
                )

                # 工具结果返回后，再次请求 LLM 生成最终 JSON
                next_response = await self.model.chat(
                    history=self.chat_history,
                    agent_name=self.__class__.__name__,
                )
                json_str = next_response.choices[0].message.content
            else:
                json_str = msg.content

            if not json_str:
                raise ValueError("返回的 JSON 字符串为空，请检查输入内容。")

            questions_solution = repair_json(json_str)
            if questions_solution:
                ic(questions_solution)
                return ModelerToCoder(questions_solution=questions_solution)

            logger.warning(
                f"JSON 解析失败 (第{attempt + 1}/{self.max_retries + 1}次)，请求模型重新生成"
            )
            await self.append_chat_history({"role": "assistant", "content": json_str})
            await self.append_chat_history(
                {
                    "role": "user",
                    "content": '你返回的JSON格式有误，请严格按照JSON格式重新输出，注意字符串值内的双引号必须转义为\\"，不要包含未转义的特殊字符。',
                }
            )

        raise ValueError(
            f"ModelerAgent 超过最大重试次数({self.max_retries})，无法解析 JSON 响应"
        )
