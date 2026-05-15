"""Agent 基类模块，提供对话管理和记忆压缩功能。"""

from typing import Any
from app.core.llm.llm import LLM, simple_chat
from app.utils.log_util import logger

# TODO: 评估任务完成情况，rethinking

# 每个字符估算的 token 数（中英混合文本的保守估计）
_CHARS_PER_TOKEN = 3
# 触发压缩的 token 占比阈值（相对 context_window）
_DEFAULT_TOKEN_THRESHOLD_RATIO = 0.75


class Agent:
    """Agent 基类，管理对话历史、轮次控制和记忆压缩。"""

    def __init__(
        self,
        task_id: str,
        model: LLM,
        context_window: int = 128000,  # 模型上下文窗口大小（token）
        token_threshold_ratio: float = _DEFAULT_TOKEN_THRESHOLD_RATIO,
    ) -> None:
        self.task_id = task_id
        self.model = model
        self.chat_history: list[dict] = []  # 存储对话历史
        self.context_window = context_window
        self.token_threshold_ratio = token_threshold_ratio
        self.current_token_count = 0  # 当前历史的估算 token 数

    def _estimate_tokens(self, text: str) -> int:
        """估算文本的 token 数量。"""
        return max(1, len(text) // _CHARS_PER_TOKEN)

    def _estimate_message_tokens(self, msg: dict) -> int:
        """估算单条消息的 token 数（含结构开销）。"""
        content = msg.get("content") or ""
        # 4 token 额外开销（role、分隔符等）
        return self._estimate_tokens(content) + 4

    async def run(self, prompt: str, system_prompt: str, sub_title: str) -> Any:
        """执行 Agent 对话并返回模型响应。

        Args:
            prompt: 用户输入的提示。
            system_prompt: 系统提示词。
            sub_title: 子任务标题。

        Returns:
            模型的响应文本。
        """
        try:
            logger.info(f"{self.__class__.__name__}:开始:执行对话")

            # 更新对话历史
            await self.append_chat_history({"role": "system", "content": system_prompt})
            await self.append_chat_history({"role": "user", "content": prompt})

            # 获取历史消息用于本次对话
            response = await self.model.chat(
                history=self.chat_history,
                agent_name=self.__class__.__name__,
                sub_title=sub_title,
            )
            response_content = response.content
            self.chat_history.append({"role": "assistant", "content": response_content})

            # 使用 API 返回的实际 prompt_tokens 更新计数
            if response.usage.prompt_tokens > 0:
                self.current_token_count = response.usage.prompt_tokens
            else:
                self.current_token_count += self._estimate_message_tokens(
                    {"content": response_content}
                )

            logger.info(f"{self.__class__.__name__}:完成:执行对话")
            return response_content
        except Exception as e:
            error_msg = f"执行过程中遇到错误: {str(e)}"
            logger.error(f"Agent执行失败: {str(e)}")
            return error_msg

    async def append_chat_history(self, msg: dict) -> None:
        """向对话历史追加消息，并在必要时触发记忆压缩。

        Args:
            msg: 消息字典，需包含 role 和 content 字段。
        """
        self.chat_history.append(msg)
        self.current_token_count += self._estimate_message_tokens(msg)

        # 只有在添加非tool消息时才进行内存清理，避免在工具调用期间破坏消息结构
        if msg.get("role") != "tool":
            await self.compress_if_needed()

    async def compress_if_needed(self) -> None:
        """当 token 数超过上下文窗口阈值时，使用 LLM 总结压缩历史。"""
        threshold = int(self.context_window * self.token_threshold_ratio)
        if self.current_token_count <= threshold:
            return

        logger.info(
            f"{self.__class__.__name__}:触发记忆压缩，"
            f"当前 token ~{self.current_token_count}，阈值 {threshold}"
        )

        try:
            # 保留第一条系统消息
            system_msg = (
                self.chat_history[0]
                if self.chat_history and self.chat_history[0]["role"] == "system"
                else None
            )

            # 查找需要保留的消息范围 - 保留最后几条完整的对话和工具调用
            preserve_start_idx = self._find_safe_preserve_point()

            # 确定需要总结的消息范围
            start_idx = 1 if system_msg else 0
            end_idx = preserve_start_idx

            if end_idx > start_idx:
                # 构造总结提示
                summarize_history = []
                if system_msg:
                    summarize_history.append(system_msg)

                summarize_history.append(
                    {
                        "role": "user",
                        "content": f"请简洁总结以下对话的关键内容和重要结论，保留重要的上下文信息：\n\n{self._format_history_for_summary(self.chat_history[start_idx:end_idx])}",
                    }
                )

                # 调用 simple_chat 进行总结
                summary = await simple_chat(self.model, summarize_history)

                # 重构聊天历史：系统消息 + 总结 + 保留的消息
                new_history = []
                if system_msg:
                    new_history.append(system_msg)

                new_history.append(
                    {"role": "assistant", "content": f"[历史对话总结] {summary}"}
                )

                # 添加需要保留的消息（最后几条完整对话）
                new_history.extend(self.chat_history[preserve_start_idx:])

                self.chat_history = new_history

                # 重新估算 token 数
                self.current_token_count = sum(
                    self._estimate_message_tokens(m) for m in self.chat_history
                )
                logger.info(
                    f"{self.__class__.__name__}:记忆压缩完成，"
                    f"压缩至 {len(self.chat_history)} 条记录，"
                    f"约 {self.current_token_count} tokens"
                )
            else:
                logger.info(f"{self.__class__.__name__}:无需压缩，记录数量合理")

        except Exception as e:
            logger.error(f"记忆压缩失败，使用简单切片策略: {str(e)}")
            # 如果总结失败，回退到安全的策略：保留系统消息和最后几条消息，确保工具调用完整性
            safe_history = self._get_safe_fallback_history()
            self.chat_history = safe_history
            self.current_token_count = sum(
                self._estimate_message_tokens(m) for m in self.chat_history
            )

    def _find_safe_preserve_point(self) -> int:
        """找到安全的保留起始点，确保不会破坏工具调用序列。"""
        # 最少保留最后3条消息，确保基本对话完整性
        min_preserve = min(3, len(self.chat_history))
        preserve_start = len(self.chat_history) - min_preserve

        # 从后往前查找，确保不会在工具调用序列中间切断
        for i in range(preserve_start, -1, -1):
            if i >= len(self.chat_history):
                continue

            if self._is_safe_cut_point(i):
                return i

        # 如果找不到安全点，至少保留最后1条消息
        return len(self.chat_history) - 1

    def _is_safe_cut_point(self, start_idx: int) -> bool:
        """检查从指定位置开始切割是否安全（不会产生孤立的tool消息）。"""
        if start_idx >= len(self.chat_history):
            return True

        for i in range(start_idx, len(self.chat_history)):
            msg = self.chat_history[i]
            if isinstance(msg, dict) and msg.get("role") == "tool":
                tool_call_id = msg.get("tool_call_id")

                # 向前查找对应的tool_calls消息
                if tool_call_id:
                    found_tool_call = False
                    for j in range(start_idx, i):
                        prev_msg = self.chat_history[j]
                        if (
                            isinstance(prev_msg, dict)
                            and "tool_calls" in prev_msg
                            and prev_msg["tool_calls"]
                        ):
                            for tool_call in prev_msg["tool_calls"]:
                                if tool_call.get("id") == tool_call_id:
                                    found_tool_call = True
                                    break
                            if found_tool_call:
                                break

                    if not found_tool_call:
                        return False

        return True

    def _get_safe_fallback_history(self) -> list:
        """获取安全的后备历史记录，确保不会有孤立的tool消息。"""
        if not self.chat_history:
            return []

        # 保留系统消息
        safe_history = []
        if self.chat_history and self.chat_history[0]["role"] == "system":
            safe_history.append(self.chat_history[0])

        # 从后往前查找安全的消息序列
        for preserve_count in range(1, min(4, len(self.chat_history)) + 1):
            start_idx = len(self.chat_history) - preserve_count
            if self._is_safe_cut_point(start_idx):
                safe_history.extend(self.chat_history[start_idx:])
                return safe_history

        # 如果都不安全，只保留最后一条非tool消息
        for i in range(len(self.chat_history) - 1, -1, -1):
            msg = self.chat_history[i]
            if isinstance(msg, dict) and msg.get("role") != "tool":
                safe_history.append(msg)
                break

        return safe_history

    def _format_history_for_summary(self, history: list[dict]) -> str:
        """格式化历史记录用于总结。"""
        formatted = []
        for msg in history:
            role = msg["role"]
            content = msg.get("content") or ""
            if len(content) > 500:
                content = content[:500] + "..."
            formatted.append(f"{role}: {content}")
        return "\n".join(formatted)
