"""LLM Provider 抽象基类。"""

from abc import ABC, abstractmethod
from app.core.llm.types import StandardResponse


class BaseProvider(ABC):
    """LLM Provider 基类，定义统一的调用接口。"""

    @abstractmethod
    async def call(
        self,
        messages: list[dict],
        model: str,
        api_key: str,
        base_url: str | None = None,
        tools: list[dict] | None = None,
        tool_choice: str | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
    ) -> StandardResponse:
        """调用 LLM 并返回标准化响应。

        Args:
            messages: 消息历史（OpenAI 格式）。
            model: 模型 ID。
            api_key: API 密钥。
            base_url: API 基础 URL。
            tools: 工具定义列表（OpenAI 格式）。
            tool_choice: 工具选择策略。
            max_tokens: 最大生成 token 数。
            top_p: 采样温度参数。

        Returns:
            标准化响应。
        """
        ...
