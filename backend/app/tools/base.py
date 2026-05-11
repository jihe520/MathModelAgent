"""工具基类模块，提供工具注册和调用的基础设施。"""

from typing import Dict, Any, List, Callable
import inspect
from app.schemas.tool_result import ToolResult


def tool(
    name: str,
    description: str,
    parameters: Dict[str, Dict[str, Any]],
    required: List[str],
) -> Callable:
    """工具注册装饰器，为函数生成工具 schema。

    Args:
        name: 工具名称。
        description: 工具描述。
        parameters: 工具参数定义。
        required: 必需参数列表。

    Returns:
        装饰器函数。
    """

    def decorator(func):
        # Create tool schema directly using provided parameters, without automatic extraction
        schema = {
            "type": "function",
            "function": {
                "name": name,
                "description": description,
                "parameters": {
                    "type": "object",
                    "properties": parameters,
                    "required": required,
                },
            },
        }

        # Store tool information
        func._function_name = name
        func._tool_description = description
        func._tool_schema = schema

        return func

    return decorator


class BaseTool:
    """工具基类，提供工具注册、查询和调用的通用方法。"""

    name: str = ""

    def __init__(self):
        pass
        self._tools_cache = None

    def get_tools(self) -> List[Dict[str, Any]]:
        """获取所有已注册的工具 schema 列表。"""
        if self._tools_cache is not None:
            return self._tools_cache

        tools = []
        for _, method in inspect.getmembers(self, inspect.ismethod):
            schema = getattr(method, "_tool_schema", None)
            if schema is not None:
                tools.append(schema)

        self._tools_cache = tools
        return tools

    def has_function(self, function_name: str) -> bool:
        """检查指定名称的工具是否存在。

        Args:
            function_name: 工具函数名称。

        Returns:
            工具是否存在。
        """
        for _, method in inspect.getmembers(self, inspect.ismethod):
            fn_name = getattr(method, "_function_name", None)
            if fn_name == function_name:
                return True
        return False

    async def invoke_function(self, function_name: str, **kwargs) -> ToolResult:
        """调用指定的工具函数。

        Args:
            function_name: 工具函数名称。
            **kwargs: 传递给工具的参数。

        Returns:
            工具调用结果。

        Raises:
            ValueError: 工具不存在时抛出。
        """
        for _, method in inspect.getmembers(self, inspect.ismethod):
            fn_name = getattr(method, "_function_name", None)
            if fn_name == function_name:
                return await method(**kwargs)

        raise ValueError(f"Tool '{function_name}' not found")
