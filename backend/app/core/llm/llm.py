"""LLM 交互模块，封装大语言模型的调用、重试和消息发送。"""

from typing import Any
from app.utils.common_utils import transform_link, split_footnotes
from app.utils.log_util import logger
import time
from app.schemas.response import (
    CoderMessage,
    WriterMessage,
    ModelerMessage,
    SystemMessage,
    CoordinatorMessage,
)
from app.services.redis_manager import redis_manager
from litellm import acompletion  # type: ignore[import-unresolved]
import litellm  # type: ignore[import-unresolved]
from app.schemas.enums import AgentType
from app.utils.track import agent_metrics
from icecream import ic  # type: ignore[import-unresolved]

litellm.callbacks = [agent_metrics]

class LLM:
    """大语言模型封装类，提供对话调用、重试和工具调用验证功能。"""
    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        base_url: str | None = None,
        task_id: str = "",
        max_tokens: int | None = None,
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.chat_count = 0
        self.max_tokens = max_tokens
        self.task_id = task_id

    def _validate_config(self, agent_name: str) -> None:
        """验证 LLM 配置是否完整。

        Args:
            agent_name: Agent 类型名称，用于错误提示。

        Raises:
            ValueError: 模型 ID 或 API Key 未配置时抛出。
        """
        if not self.model or not str(self.model).strip():
            raise ValueError(f"{agent_name} 未配置模型 ID，请设置对应的 *_MODEL")
        if not self.api_key or not str(self.api_key).strip():
            raise ValueError(f"{agent_name} 未配置 API Key，请设置对应的 *_API_KEY")

    async def chat(
        self,
        history: list | None = None,
        tools: list | None = None,
        tool_choice: str | None = None,
        max_retries: int | None = None,  # 最大重试次数，None表示无限制
        retry_delay: float = 1.0,  # 添加重试延迟
        top_p: float | None = None,  # 添加top_p参数,
        agent_name: str = "SystemAgent",  # CoderAgent or WriterAgent
        sub_title: str | None = None,
    ) -> Any:
        logger.info(f"subtitle是:{sub_title}")
        self._validate_config(agent_name)

        # 验证和修复工具调用完整性
        if history:
            history = self._validate_and_fix_tool_calls(history)

        kwargs = {
            "api_key": self.api_key,
            "model": self.model,
            "messages": history,
            "stream": False,
            "top_p": top_p,
            "metadata": {"agent_name": agent_name},
        }

        if tools:
            kwargs["tools"] = tools
            kwargs["tool_choice"] = tool_choice

        if self.max_tokens:
            kwargs["max_tokens"] = self.max_tokens

        if self.base_url:
            kwargs["base_url"] = self.base_url
        litellm.enable_json_schema_validation = True #加入json格式验证

        # TODO: stream 输出
        attempt = 0
        while True:
            try:
                response = await acompletion(**kwargs)
                logger.info(f"API返回: {response}")
                if not response or not hasattr(response, "choices"):
                    raise ValueError("无效的API响应")
                self.chat_count += 1
                await self.send_message(response, agent_name, sub_title)
                return response
            except Exception as e:
                attempt += 1
                logger.error(f"第{attempt}次重试: {str(e)}")
                if max_retries is not None and attempt >= max_retries:
                    logger.debug(f"请求参数: {kwargs}")
                    raise
                time.sleep(retry_delay * min(attempt, 10))  # 指数退避，上限10秒

    def _validate_and_fix_tool_calls(self, history: list) -> list:
        """验证并修复工具调用完整性"""
        if not history:
            return history

        ic(f"🔍 开始验证工具调用，历史消息数量: {len(history)}")

        # 查找所有未匹配的tool_calls
        fixed_history = []
        i = 0

        while i < len(history):
            msg = history[i]

            # 如果是包含tool_calls的消息
            if isinstance(msg, dict) and "tool_calls" in msg and msg["tool_calls"]:
                ic(f"📞 发现tool_calls消息在位置 {i}")

                # 检查每个tool_call是否都有对应的response，分别处理
                valid_tool_calls = []
                invalid_tool_calls = []

                for tool_call in msg["tool_calls"]:
                    tool_call_id = tool_call.get("id")
                    ic(f"  检查tool_call_id: {tool_call_id}")

                    if tool_call_id:
                        # 查找对应的tool响应
                        found_response = False
                        for j in range(i + 1, len(history)):
                            if (
                                history[j].get("role") == "tool"
                                and history[j].get("tool_call_id") == tool_call_id
                            ):
                                ic(f"  ✅ 找到匹配响应在位置 {j}")
                                found_response = True
                                break

                        if found_response:
                            valid_tool_calls.append(tool_call)
                        else:
                            ic(f"  ❌ 未找到匹配响应: {tool_call_id}")
                            invalid_tool_calls.append(tool_call)

                # 根据检查结果处理消息
                if valid_tool_calls:
                    # 有有效的tool_calls，保留它们
                    fixed_msg = msg.copy()
                    fixed_msg["tool_calls"] = valid_tool_calls
                    fixed_history.append(fixed_msg)
                    ic(
                        f"  🔧 保留 {len(valid_tool_calls)} 个有效tool_calls，移除 {len(invalid_tool_calls)} 个无效的"
                    )
                else:
                    # 没有有效的tool_calls，移除tool_calls但可能保留其他内容
                    cleaned_msg = {k: v for k, v in msg.items() if k != "tool_calls"}
                    if cleaned_msg.get("content"):
                        fixed_history.append(cleaned_msg)
                        ic("  🔧 移除所有tool_calls，保留消息内容")
                    else:
                        ic("  🗑️ 完全移除空的tool_calls消息")

            # 如果是tool响应消息，检查是否是孤立的
            elif isinstance(msg, dict) and msg.get("role") == "tool":
                tool_call_id = msg.get("tool_call_id")
                ic(f"🔧 检查tool响应消息: {tool_call_id}")

                # 查找对应的tool_calls
                found_call = False
                for j in range(len(fixed_history)):
                    if fixed_history[j].get("tool_calls") and any(
                        tc.get("id") == tool_call_id
                        for tc in fixed_history[j]["tool_calls"]
                    ):
                        found_call = True
                        break

                if found_call:
                    fixed_history.append(msg)
                    ic("  ✅ 保留有效的tool响应")
                else:
                    ic(f"  🗑️ 移除孤立的tool响应: {tool_call_id}")

            else:
                # 普通消息，直接保留
                fixed_history.append(msg)

            i += 1

        if len(fixed_history) != len(history):
            ic(f"🔧 修复完成: {len(history)} -> {len(fixed_history)} 条消息")
        else:
            ic("✅ 验证通过，无需修复")

        return fixed_history

    async def send_message(self, response, agent_name, sub_title=None):
        """将 LLM 响应通过 Redis 发送给前端。

        Args:
            response: LLM 返回的响应对象。
            agent_name: Agent 类型。
            sub_title: 子任务标题。
        """
        logger.info(f"subtitle是:{sub_title}")
        content = response.choices[0].message.content

        # tool_call 响应的 content 为 None，跳过消息发送
        if content is None:
            return

        agent_msg: Any = None
        match agent_name:
            case AgentType.CODER:
                agent_msg = CoderMessage(content=content)
            case AgentType.WRITER:
                # 处理 Markdown 格式的图片语法
                content, _ = split_footnotes(content)
                content = transform_link(self.task_id, content)
                agent_msg = WriterMessage(
                    content=content,
                    sub_title=sub_title,
                )
            case AgentType.MODELER:
                agent_msg = ModelerMessage(content=content)
            case AgentType.SYSTEM:
                agent_msg = SystemMessage(content=content)
            case AgentType.COORDINATOR:
                agent_msg = CoordinatorMessage(content=content)
            case _:
                raise ValueError(f"不支持的agent类型: {agent_name}")

        await redis_manager.publish_message(
            self.task_id,
            agent_msg,
        )


# class DeepSeekModel(LLM):
#     def __init__(
#         self,
#         api_key: str,
#         model: str,
#         base_url: str,
#         task_id: str,
#     ):
#         super().__init__(api_key, model, base_url, task_id)
# self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)


async def simple_chat(model: LLM, history: list) -> str:
    """使用 LLM 进行简单的单轮对话。

    Args:
        model: LLM 实例。
        history: 构造好的历史记录（包含 system_prompt 和 user_prompt）。

    Returns:
        模型的响应文本。
    """
    kwargs = {
        "api_key": model.api_key,
        "model": model.model,
        "messages": history,
        "stream": False,
    }

    if model.base_url:
        kwargs["base_url"] = model.base_url

    response = await acompletion(**kwargs)

    return response.choices[0].message.content
