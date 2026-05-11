"""代码解释器抽象基类模块。"""

import abc
import re
from app.tools.notebook_serializer import NotebookSerializer
from app.services.redis_manager import redis_manager
from app.utils.log_util import logger
from app.schemas.response import (
    OutputItem,
    InterpreterMessage,
)


class BaseCodeInterpreter(abc.ABC):
    """代码解释器抽象基类，定义代码执行、输出管理和资源清理的接口。"""
    def __init__(
        self,
        task_id: str,
        work_dir: str,
        notebook_serializer: NotebookSerializer,
    ):
        self.task_id = task_id
        self.work_dir = work_dir
        self.notebook_serializer = notebook_serializer
        self.section_output: dict[str, dict[str, list[str]]] = {}
        self.last_created_images = set()

    @abc.abstractmethod
    async def initialize(self):
        """初始化解释器，必要时上传文件、启动内核等"""
        ...

    @abc.abstractmethod
    async def _pre_execute_code(self):
        """执行初始化代码"""
        ...

    @abc.abstractmethod
    async def execute_code(self, code: str) -> tuple[str, bool, str]:
        """执行一段代码，返回 (输出文本, 是否出错, 错误信息)"""
        ...

    @abc.abstractmethod
    async def cleanup(self):
        """清理资源，比如关闭沙箱或内核"""
        ...

    @abc.abstractmethod
    async def get_created_images(self, section: str) -> list[str]:
        """获取当前 section 创建的图片列表"""
        ...

    async def _push_to_websocket(self, content_to_display: list[OutputItem] | None):
        logger.info("执行结果已推送到WebSocket")

        agent_msg = InterpreterMessage(
            output=content_to_display,
        )
        logger.debug(f"发送消息: {agent_msg.model_dump_json()}")
        await redis_manager.publish_message(
            self.task_id,
            agent_msg,
        )

    def add_section(self, section_name: str) -> None:
        """确保添加的section结构正确"""

        if section_name not in self.section_output:
            self.section_output[section_name] = {"content": [], "images": []}

    def add_content(self, section: str, text: str) -> None:
        """向指定section添加文本内容"""
        self.add_section(section)
        self.section_output[section]["content"].append(text)

    def get_code_output(self, section: str) -> str:
        """获取指定section的代码输出"""
        return "\n".join(self.section_output[section]["content"])

    def delete_color_control_char(self, string):
        ansi_escape = re.compile(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]")
        return ansi_escape.sub("", string)

    def _truncate_text(self, text: str, max_length: int = 1000) -> str:
        """截断文本，保留开头和结尾的重要信息"""
        if len(text) <= max_length:
            return text

        half_length = max_length // 2
        return text[:half_length] + "\n... (内容已截断) ...\n" + text[-half_length:]
