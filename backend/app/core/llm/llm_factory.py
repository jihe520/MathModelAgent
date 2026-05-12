"""LLM 工厂模块，根据配置创建各 Agent 使用的 LLM 实例。"""

from app.config.setting import settings
from app.core.llm.llm import LLM


class LLMFactory:
    """LLM 工厂类，根据配置创建协调者、建模手、代码手和写作手的 LLM 实例。"""
    task_id: str

    def __init__(self, task_id: str) -> None:
        self.task_id = task_id

    def get_all_llms(self) -> tuple[LLM, LLM, LLM, LLM]:
        """创建所有 Agent 的 LLM 实例。

        Returns:
            包含 (coordinator_llm, modeler_llm, coder_llm, writer_llm) 的元组。
        """
        coordinator_llm = LLM(
            api_key=settings.COORDINATOR_API_KEY,
            model=settings.COORDINATOR_MODEL,
            base_url=settings.COORDINATOR_BASE_URL,
            task_id=self.task_id,
            max_tokens=settings.COORDINATOR_MAX_TOKENS,
        )

        modeler_llm = LLM(
            api_key=settings.MODELER_API_KEY,
            model=settings.MODELER_MODEL,
            base_url=settings.MODELER_BASE_URL,
            task_id=self.task_id,
            max_tokens=settings.MODELER_MAX_TOKENS,
        )

        coder_llm = LLM(
            api_key=settings.CODER_API_KEY,
            model=settings.CODER_MODEL,
            base_url=settings.CODER_BASE_URL,
            task_id=self.task_id,
            max_tokens=settings.CODER_MAX_TOKENS,
        )

        writer_llm = LLM(
            api_key=settings.WRITER_API_KEY,
            model=settings.WRITER_MODEL,
            base_url=settings.WRITER_BASE_URL,
            task_id=self.task_id,
            max_tokens=settings.WRITER_MAX_TOKENS,
        )

        return coordinator_llm, modeler_llm, coder_llm, writer_llm

    def get_fallback_llms(self) -> dict[str, LLM | None]:
        """创建所有 Agent 的 Fallback LLM 实例。

        仅当对应 FALLBACK_*_API_KEY 和 FALLBACK_*_MODEL 均配置时才创建实例，
        否则返回 None，表示该 Agent 无 fallback。

        Returns:
            以 Agent 名称为键、LLM 实例或 None 为值的字典。
        """
        fallbacks: dict[str, LLM | None] = {}

        agent_configs = [
            ("coordinator", settings.FALLBACK_COORDINATOR_API_KEY, settings.FALLBACK_COORDINATOR_MODEL, settings.FALLBACK_COORDINATOR_BASE_URL, settings.FALLBACK_COORDINATOR_MAX_TOKENS),
            ("modeler", settings.FALLBACK_MODELER_API_KEY, settings.FALLBACK_MODELER_MODEL, settings.FALLBACK_MODELER_BASE_URL, settings.FALLBACK_MODELER_MAX_TOKENS),
            ("coder", settings.FALLBACK_CODER_API_KEY, settings.FALLBACK_CODER_MODEL, settings.FALLBACK_CODER_BASE_URL, settings.FALLBACK_CODER_MAX_TOKENS),
            ("writer", settings.FALLBACK_WRITER_API_KEY, settings.FALLBACK_WRITER_MODEL, settings.FALLBACK_WRITER_BASE_URL, settings.FALLBACK_WRITER_MAX_TOKENS),
        ]

        for name, api_key, model, base_url, max_tokens in agent_configs:
            if api_key and model:
                fallbacks[name] = LLM(
                    api_key=api_key,
                    model=model,
                    base_url=base_url,
                    task_id=self.task_id,
                    max_tokens=max_tokens,
                )
            else:
                fallbacks[name] = None

        return fallbacks

    def get_evaluator_llm(self) -> LLM | None:
        """创建评估器的 LLM 实例。

        仅当 EVALUATOR_API_KEY 和 EVALUATOR_MODEL 均配置时才创建实例。

        Returns:
            LLM 实例，未配置时返回 None。
        """
        if settings.EVALUATOR_API_KEY and settings.EVALUATOR_MODEL:
            return LLM(
                api_key=settings.EVALUATOR_API_KEY,
                model=settings.EVALUATOR_MODEL,
                base_url=settings.EVALUATOR_BASE_URL,
                task_id=self.task_id,
            )
        return None
