"""工具调用结果数据模型。"""

from pydantic import BaseModel
from typing import Any, Optional


class ToolResult(BaseModel):
    """工具调用的通用返回结构。"""
    success: bool
    message: Optional[str] = None
    data: Optional[Any] = None
