"""OpenAI Responses API Provider。"""

from openai import AsyncOpenAI
from app.core.llm.providers.base import BaseProvider
from app.core.llm.types import StandardResponse, ToolCall, Usage


class OpenAIResponsesProvider(BaseProvider):
    """OpenAI Responses API (/v1/responses) 实现。"""

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

        input_items = self._messages_to_input(messages)

        kwargs: dict = {"model": model, "input": input_items}
        if max_tokens:
            kwargs["max_output_tokens"] = max_tokens
        if top_p is not None:
            kwargs["top_p"] = top_p
        if tools:
            kwargs["tools"] = self._convert_tools(tools)
            if tool_choice:
                kwargs["tool_choice"] = self._convert_tool_choice(tool_choice)

        response = await client.responses.create(**kwargs)

        content_parts: list[str] = []
        tool_calls: list[ToolCall] = []

        for item in response.output:
            if item.type == "message":
                for part in item.content:
                    if part.type == "output_text":
                        content_parts.append(part.text)
            elif item.type == "function_call":
                tool_calls.append(ToolCall(
                    id=item.call_id,
                    name=item.name,
                    arguments=item.arguments,
                ))

        content = "".join(content_parts) if content_parts else None

        usage = Usage(
            prompt_tokens=response.usage.input_tokens if response.usage else 0,
            completion_tokens=response.usage.output_tokens if response.usage else 0,
        )

        return StandardResponse(content=content, tool_calls=tool_calls, usage=usage)

    def _messages_to_input(self, messages: list[dict]) -> list[dict]:
        """将 Chat Completions messages 格式转为 Responses input 格式。"""
        input_items = []
        for msg in messages:
            role = msg.get("role", "user")
            if role == "system":
                input_items.append({"role": "developer", "content": msg["content"]})
            elif role == "tool":
                input_items.append({
                    "type": "function_call_output",
                    "call_id": msg.get("tool_call_id", ""),
                    "output": msg.get("content", ""),
                })
            elif role == "assistant" and "tool_calls" in msg:
                for tc in msg["tool_calls"]:
                    input_items.append({
                        "type": "function_call",
                        "call_id": tc["id"],
                        "name": tc["function"]["name"],
                        "arguments": tc["function"]["arguments"],
                    })
                if msg.get("content"):
                    input_items.append({"role": "assistant", "content": msg["content"]})
            else:
                input_items.append({"role": role, "content": msg.get("content", "")})
        return input_items

    def _convert_tools(self, tools: list[dict]) -> list[dict]:
        """将 Chat Completions tools 格式转为 Responses tools 格式。"""
        converted = []
        for tool in tools:
            if tool.get("type") == "function":
                func = tool["function"]
                converted.append({
                    "type": "function",
                    "name": func["name"],
                    "description": func.get("description", ""),
                    "parameters": func.get("parameters", {}),
                    "strict": func.get("strict", True),
                })
        return converted

    def _convert_tool_choice(self, tool_choice: str) -> str | dict:
        """转换 tool_choice 格式。"""
        if tool_choice == "auto":
            return "auto"
        if tool_choice == "none":
            return "none"
        if tool_choice == "required":
            return {"type": "function"}
        return tool_choice
