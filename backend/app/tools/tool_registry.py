"""工具注册与分发模块，替代各 Agent 中的 if/elif 硬编码分发。"""

from typing import Callable, Awaitable
from app.utils.log_util import logger


class ToolRegistry:
    """统一工具注册表，管理 tool schema 和 handler 分发。"""

    def __init__(self) -> None:
        self._handlers: dict[str, Callable[..., Awaitable[str]]] = {}
        self._schemas: dict[str, dict] = {}

    def register(
        self,
        name: str,
        handler: Callable[..., Awaitable[str]],
        schema: dict,
    ) -> None:
        """注册工具。

        Args:
            name: 工具名称，需与 schema 中的 function.name 一致。
            handler: 异步处理函数，签名 (arguments: dict, task_id: str) -> str。
            schema: OpenAI function-calling 格式的 tool schema。
        """
        self._handlers[name] = handler
        self._schemas[name] = schema
        logger.info(f"ToolRegistry: 注册工具 {name}")

    def get_schemas(self, names: list[str] | None = None) -> list[dict]:
        """获取指定工具的 OpenAI function-calling schema 列表。

        Args:
            names: 工具名称列表，None 表示返回所有已注册工具。

        Returns:
            schema 列表。
        """
        if names is None:
            return list(self._schemas.values())
        return [self._schemas[n] for n in names if n in self._schemas]

    async def dispatch(self, name: str, arguments: dict, task_id: str) -> str:
        """分发工具调用到对应 handler。

        Args:
            name: 工具名称。
            arguments: 工具参数。
            task_id: 当前任务 ID。

        Returns:
            工具执行结果字符串。

        Raises:
            ValueError: 工具未注册时抛出。
        """
        handler = self._handlers.get(name)
        if handler is None:
            raise ValueError(f"ToolRegistry: 未注册的工具 {name}")
        logger.info(f"ToolRegistry: 分发工具调用 {name}")
        return await handler(arguments, task_id)


# 全局单例
tool_registry = ToolRegistry()
