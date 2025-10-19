from app.core.agents.agent import Agent
from app.core.llm.llm import LLM
from app.config.setting import settings
from app.core.prompts import MODELER_PROMPT
from app.schemas.A2A import CoordinatorToModeler, ModelerToCoder
from icecream import ic
from json_repair import repair_json
import json

# TODO: 提问工具tool


class ModelerAgent(Agent):  # 继承自Agent类
    def __init__(
        self,
        task_id: str,
        model: LLM,
        max_chat_turns: int = settings.MAX_CHAT_TURNS,  # 添加最大对话轮次限制
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

        response = await self.model.chat(
            history=self.chat_history,
            agent_name=self.__class__.__name__,
        )

        json_str = response.choices[0].message.content

        json_str = json_str.replace("```json", "").replace("```", "").strip()

        if not json_str:
            raise ValueError("返回的 JSON 字符串为空，请检查输入内容。")
        try:
            questions_solution = json.loads(repair_json(json_str))
            ic(questions_solution)
            return ModelerToCoder(questions_solution=questions_solution)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON 解析错误: {e}")
