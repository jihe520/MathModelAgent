"""Anthropic Messages API Provider。"""

import json as _json
from anthropic import AsyncAnthropic
from app.core.llm.providers.base import BaseProvider
from app.core.llm.types import StandardResponse, ToolCall, Usage


class AnthropicProvider(BaseProvider):
    """Anthropic Messages API (/v1/messages) 实现。"""

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
        client = AsyncAnthropic(api_key=api_key, base_url=base_url)

        system_prompt, anthropic_messages = self._convert_messages(messages)

        kwargs: dict = {
            "model": model,
            "messages": anthropic_messages,
            "max_tokens": max_tokens or 4096,
        }
        if system_prompt:
            kwargs["system"] = system_prompt
        if top_p is not None:
            kwargs["top_p"] = top_p
        if tools:
            kwargs["tools"] = self._convert_tools(tools)
            if tool_choice:
                kwargs["tool_choice"] = self._convert_tool_choice(tool_choice)

        response = await client.messages.create(**kwargs)

        content_parts: list[str] = []
        tool_calls: list[ToolCall] = []

        for block in response.content:
            if block.type == "text":
                content_parts.append(block.text)
            elif block.type == "tool_use":
                tool_calls.append(ToolCall(
                    id=block.id,
                    name=block.name,
                    arguments=_json.dumps(block.input),
                ))

        content = "".join(content_parts) if content_parts else None

        usage = Usage(
            prompt_tokens=response.usage.input_tokens,
            completion_tokens=response.usage.output_tokens,
        )

        return StandardResponse(content=content, tool_calls=tool_calls, usage=usage)

    def _convert_messages(self, messages: list[dict]) -> tuple[str | None, list[dict]]:
        """将 OpenAI 格式 messages 转为 Anthropic 格式。"""
        system_prompt = None
        converted: list[dict] = []

        for msg in messages:
            role = msg.get("role", "user")

            if role == "system" and system_prompt is None:
                system_prompt = msg["content"]
                continue

            if role == "assistant" and "tool_calls" in msg and msg["tool_calls"]:
                content_blocks: list[dict] = []
                if msg.get("content"):
                    content_blocks.append({"type": "text", "text": msg["content"]})
                for tc in msg["tool_calls"]:
                    content_blocks.append({
                        "type": "tool_use",
                        "id": tc["id"],
                        "name": tc["function"]["name"],
                        "input": _json.loads(tc["function"]["arguments"]),
                    })
                converted.append({"role": "assistant", "content": content_blocks})
                continue

            if role == "tool":
                converted.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": msg.get("tool_call_id", ""),
                        "content": msg.get("content", ""),
                    }],
                })
                continue

            converted.append(msg)

        return system_prompt, converted

    def _convert_tools(self, tools: list[dict]) -> list[dict]:
        """将 OpenAI tools 格式转为 Anthropic 格式。"""
        converted = []
        for tool in tools:
            if tool.get("type") == "function":
                func = tool["function"]
                converted.append({
                    "name": func["name"],
                    "description": func.get("description", ""),
                    "input_schema": func.get("parameters", {}),
                })
        return converted

    def _convert_tool_choice(self, tool_choice: str) -> dict:
        """转换 tool_choice 为 Anthropic 格式。"""
        if tool_choice == "auto":
            return {"type": "auto"}
        if tool_choice == "none":
            return {"type": "none"}
        if tool_choice == "required":
            return {"type": "any"}
        return {"type": "auto"}
