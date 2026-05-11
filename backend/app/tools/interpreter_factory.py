"""代码解释器工厂模块，根据配置创建本地或远程解释器。"""

from typing import Literal
from app.tools.base_interpreter import BaseCodeInterpreter
from app.tools.e2b_interpreter import E2BCodeInterpreter
from app.tools.local_interpreter import LocalCodeInterpreter
from app.tools.notebook_serializer import NotebookSerializer
from app.config.setting import settings
from app.utils.log_util import logger


async def create_interpreter(
    kind: Literal["remote", "local"] = "local",
    *,
    task_id: str,
    work_dir: str,
    notebook_serializer: NotebookSerializer,
    timeout=3000,
):
    """创建代码解释器实例。

    Args:
        kind: 解释器类型，"remote" 使用 E2B 沙箱，"local" 使用本地 Jupyter。
        task_id: 任务 ID。
        work_dir: 工作目录。
        notebook_serializer: Notebook 序列化器。
        timeout: 超时时间（秒）。

    Returns:
        初始化完成的代码解释器实例。

    Raises:
        ValueError: 未知的解释器类型时抛出。
    """
    if not settings.E2B_API_KEY:
        logger.info("默认使用本地解释器")
        kind = "local"
    else:
        logger.info("使用远程解释器")
        kind = "remote"

    interp: BaseCodeInterpreter
    if kind == "remote":
        interp = await E2BCodeInterpreter.create(
            task_id=task_id,
            work_dir=work_dir,
            notebook_serializer=notebook_serializer,
        )
        await interp.initialize(timeout=timeout)  # type: ignore[reportCallIssue]
        return interp
    elif kind == "local":
        interp = LocalCodeInterpreter(
            task_id=task_id,
            work_dir=work_dir,
            notebook_serializer=notebook_serializer,
        )
        await interp.initialize()
        return interp
    else:
        raise ValueError(f"未知 interpreter 类型：{kind}")
