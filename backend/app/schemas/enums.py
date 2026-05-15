"""枚举类型定义模块。"""

from enum import Enum


class CompTemplate(str, Enum):
    """竞赛模板类型。"""
    CHINA = "CHINA"
    AMERICAN = "AMERICAN"


class FormatOutPut(str, Enum):
    """输出格式类型。"""
    Markdown = "Markdown"
    LaTeX = "LaTeX"


class AgentType(str, Enum):
    """Agent 类型标识。"""
    COORDINATOR = "CoordinatorAgent"
    MODELER = "ModelerAgent"
    CODER = "CoderAgent"
    WRITER = "WriterAgent"
    SYSTEM = "SystemAgent"


class AgentStatus(str, Enum):
    """Agent 执行状态。"""
    START = "start"
    WORKING = "working"
    DONE = "done"
    ERROR = "error"
    SUCCESS = "success"
