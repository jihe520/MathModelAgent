"""OpenAI Chat Completions API Provider。"""

from openai import AsyncOpenAI
from app.core.llm.providers.base import BaseProvider
from app.core.llm.types import StandardResponse, ToolCall, Usage


class OpenAIChatProvider(BaseProvider):
    """OpenAI Chat Completions API (/v1/chat/completions) 实现。"""

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
        client = AsyncOpenAI(api_key=api_key, base_url=base_url)

        kwargs: dict = {"model": model, "messages": messages}
        if max_tokens:
            kwargs["max_tokens"] = max_tokens
        if top_p is not None:
            kwargs["top_p"] = top_p
        if tools:
            kwargs["tools"] = tools
            if tool_choice:
                kwargs["tool_choice"] = tool_choice

        response = await client.chat.completions.create(**kwargs)

        choice = response.choices[0]
        message = choice.message

        tool_calls: list[ToolCall] = []
        for tc in message.tool_calls or []:
            tool_calls.append(ToolCall(
                id=tc.id,
                name=tc.function.name,
                arguments=tc.function.arguments,
            ))

        usage = Usage(
            prompt_tokens=response.usage.prompt_tokens if response.usage else 0,
            completion_tokens=response.usage.completion_tokens if response.usage else 0,
        )

        reasoning = getattr(message, "reasoning_content", None)
        return StandardResponse(
            content=message.content,
            reasoning_content=reasoning,
            tool_calls=tool_calls,
            usage=usage,
        )
