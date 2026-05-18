"""协调者 Agent 模块，负责识别用户意图并拆解数学建模问题。"""

import asyncio
from app.core.agents.agent import Agent
from app.core.llm.llm import LLM
from app.core.prompts import COORDINATOR_PROMPT
import json
import re
from app.utils.log_util import logger
from app.schemas.A2A import CoordinatorToModeler


class CoordinatorAgent(Agent):
    """协调者 Agent，判断用户输入是否为数学建模问题并拆解为结构化问题列表。"""
    def __init__(
        self,
        task_id: str,
        model: LLM,
        context_window: int = 128000,
        cancel_event: asyncio.Event | None = None,
    ) -> None:
        super().__init__(task_id, model, context_window, cancel_event=cancel_event)
        self.system_prompt = COORDINATOR_PROMPT

    async def run(self, ques_all: str) -> CoordinatorToModeler:  # type: ignore[reportIncompatibleMethodOverride]
        """解析用户输入的问题并格式化为结构化 JSON。

        Args:
            ques_all: 用户输入的完整题目信息。

        Returns:
            CoordinatorToModeler 对象，包含结构化问题和问题数量。
        """
        await self.append_chat_history(
            {"role": "system", "content": self.system_prompt}
        )
        await self.append_chat_history({"role": "user", "content": ques_all})
        attempt = 0
        while True:
            try:
                response = await self._chat(
                    history=self.chat_history,
                    agent_name=self.__class__.__name__,
                )
                json_str = response.content or ""

                # 清理 JSON 字符串
                json_str = json_str.replace("```json", "").replace("```", "").strip()
                json_str = re.sub(r"[\x00-\x1F\x7F]", "", json_str)

                if not json_str:
                    raise ValueError("返回的 JSON 字符串为空")

                questions = json.loads(json_str)
                ques_count = questions["ques_count"]
                logger.info(f"questions:{questions}")
                return CoordinatorToModeler(questions=questions, ques_count=ques_count)

            except (json.JSONDecodeError, ValueError, KeyError) as e:
                attempt += 1
                logger.warning(f"解析失败 (尝试 {attempt}): {str(e)}")

                # 添加错误反馈提示
                error_prompt = f"⚠️ 上次响应格式错误: {str(e)}。请严格输出JSON格式"
                await self.append_chat_history({
                    "role": "system",
                    "content": self.system_prompt + "\n" + error_prompt
                })
