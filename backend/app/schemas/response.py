"""响应数据模型定义，包括消息类型和代码执行结果。"""

from typing import Literal, Union
from app.schemas.enums import AgentType
from pydantic import BaseModel, Field
from uuid import uuid4


class Message(BaseModel):
    """消息基类。"""
    id: str = Field(default_factory=lambda: str(uuid4()))
    msg_type: Literal[
        "system", "agent", "user", "tool"
    ]  # system msg | agent message | user message | tool message
    content: str | None = None


class ToolMessage(Message):
    msg_type: Literal["system", "agent", "user", "tool"] = "tool"
    tool_name: Literal["execute_code", "search_scholar"]
    input: dict | None = None
    output: list | None = None


class SystemMessage(Message):
    msg_type: Literal["system", "agent", "user", "tool"] = "system"
    type: Literal["info", "warning", "success", "error"] = "info"


class UserMessage(Message):
    msg_type: Literal["system", "agent", "user", "tool"] = "user"


class AgentMessage(Message):
    msg_type: Literal["system", "agent", "user", "tool"] = "agent"
    agent_type: AgentType  # CoordinatorAgent | ModelerAgent | CoderAgent | WriterAgent


class ModelerMessage(AgentMessage):
    agent_type: AgentType = AgentType.MODELER


class CoordinatorMessage(AgentMessage):
    agent_type: AgentType = AgentType.COORDINATOR


class CodeExecution(BaseModel):
    """代码执行结果基类。"""
    res_type: Literal["stdout", "stderr", "result", "error"]
    msg: str | None = None


class StdOutModel(CodeExecution):
    res_type: Literal["stdout", "stderr", "result", "error"] = "stdout"


class StdErrModel(CodeExecution):
    res_type: Literal["stdout", "stderr", "result", "error"] = "stderr"


class ResultModel(CodeExecution):
    res_type: Literal["stdout", "stderr", "result", "error"] = "result"
    format: Literal[
        "text",
        "html",
        "markdown",
        "png",
        "jpeg",
        "svg",
        "pdf",
        "latex",
        "json",
        "javascript",
    ]


class ErrorModel(CodeExecution):
    res_type: Literal["stdout", "stderr", "result", "error"] = "error"
    name: str
    value: str
    traceback: str


# 代码执行结果类型
OutputItem = Union[StdOutModel, StdErrModel, ResultModel, ErrorModel]


class ScholarMessage(ToolMessage):
    tool_name: Literal["execute_code", "search_scholar"] = "search_scholar"
    input: dict | None = None  # query
    output: list[str] | None = None  # cites


class InterpreterMessage(ToolMessage):
    tool_name: Literal["execute_code", "search_scholar"] = "execute_code"
    input: dict | None = None  # code
    output: list[OutputItem] | None = None  # code_results


# 1. 只带 code
# 2. 只带 code result
class CoderMessage(AgentMessage):
    agent_type: AgentType = AgentType.CODER


class WriterMessage(AgentMessage):
    agent_type: AgentType = AgentType.WRITER
    sub_title: str | None = None


# 所有可能的消息类型
MessageType = Union[
    SystemMessage,
    UserMessage,
    ModelerMessage,
    CoderMessage,
    WriterMessage,
    CoordinatorMessage,
]
