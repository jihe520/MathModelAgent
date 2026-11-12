"""boxd 云端代码解释器模块，在 boxd 机器中的常驻 Jupyter 内核上执行 Python 代码。"""

import asyncio
import json
import os
import re
import uuid
from datetime import datetime
from pathlib import Path

from boxd import AsyncBoxd
from boxd.errors import ConflictError

from app.config.setting import settings
from app.schemas.response import (
    OutputItem,
    ResultModel,
    StdErrModel,
    SystemMessage,
)
from app.services.redis_manager import redis_manager
from app.tools.base_interpreter import BaseCodeInterpreter
from app.tools.matplotlib_setup import build_matplotlib_init_code
from app.tools.notebook_serializer import NotebookSerializer
from app.utils.log_util import logger

# 机器内的目录：代码在 REMOTE_WORK_DIR 中运行，内核与虚拟环境放在 REMOTE_HOME
REMOTE_WORK_DIR = "/home/boxd/work"
REMOTE_HOME = "/home/boxd/.mathmodelagent"
REMOTE_PYTHON = f"{REMOTE_HOME}/venv/bin/python"
REMOTE_RUNNER = f"{REMOTE_HOME}/kernel_runner.py"
REMOTE_CONNECTION_FILE = f"{REMOTE_HOME}/kernel.json"
REMOTE_KERNEL_PID_FILE = f"{REMOTE_HOME}/kernel.pid"

# 代码手常用的库（参照后端依赖中的数据分析与建模库）
KERNEL_PACKAGES = (
    "ipykernel",
    "jupyter_client",
    "numpy",
    "pandas",
    "scipy",
    "matplotlib",
    "seaborn",
    "scikit-learn",
    "statsmodels",
    "xgboost",
    "shap",
    "openpyxl",
)

UPLOAD_SUFFIXES = (".csv", ".xlsx", ".ttf", ".otf", ".ttc")
IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg")
RUNNER_SOURCE = Path(__file__).with_name("boxd_kernel_runner.py")
# 执行脚本的退出码：3 内核未就绪，4 内核在执行中退出
KERNEL_GONE_EXIT_CODES = (3, 4)
# 5 超时后已中断（变量保留），6 超时且内核不响应中断
CELL_TIMED_OUT_EXIT_CODE = 5
KERNEL_STUCK_EXIT_CODE = 6
# 执行脚本自己负责超时；整次调用再多等这么久仍未返回，就放弃并重启内核
EXEC_GRACE_SECONDS = 90


class KernelRestartedError(RuntimeError):
    """内核已重启，之前定义的变量全部丢失。"""


class BoxdCodeInterpreter(BaseCodeInterpreter):
    """基于 boxd 云端机器的代码解释器。

    每个任务创建一台隔离的 boxd 机器，在机器中启动常驻 Jupyter 内核，
    因此变量在多次 execute_code 之间保留，行为与本地解释器一致。
    """

    def __init__(
        self,
        task_id: str,
        work_dir: str,
        notebook_serializer: NotebookSerializer,
        *,
        client: AsyncBoxd | None = None,
        name_prefix: str = "mathmodelagent-",
    ):
        super().__init__(task_id, work_dir, notebook_serializer)
        self.client = client
        # 自己创建的客户端在 cleanup 时关闭，外部传入的由调用方管理
        self._owns_client = client is None
        self.name_prefix = name_prefix
        self.machine_id: str | None = None
        self._cell_count = 0
        self._restarting = False
        # 本实例独有的标签：创建请求出错时，用它确认机器是否其实已经建好
        self._run_label = uuid.uuid4().hex
        # 已同步到本地的远端文件：文件名 -> (大小, 修改时间)
        self._synced: dict[str, tuple[int, datetime]] = {}

    @classmethod
    async def create(
        cls,
        task_id: str,
        work_dir: str,
        notebook_serializer: NotebookSerializer,
    ) -> "BoxdCodeInterpreter":
        """创建 BoxdCodeInterpreter 实例"""
        return cls(task_id, work_dir, notebook_serializer)

    def _machine_name(self) -> str:
        """机器名：前缀加任务 ID，只保留小写字母、数字和连字符。"""
        name = re.sub(r"[^a-z0-9-]+", "-", f"{self.name_prefix}{self.task_id}".lower())
        return name.strip("-")[:63]

    async def initialize(self):
        """创建机器、准备 Python 环境、启动内核并上传数据文件。

        Raises:
            ValueError: 未配置 BOXD_API_KEY 时抛出。
        """
        if self.client is None:
            if not settings.BOXD_API_KEY:
                raise ValueError("BOXD_API_KEY 未配置，无法使用 boxd 解释器")
            self.client = AsyncBoxd(
                api_key=settings.BOXD_API_KEY, region=settings.BOXD_REGION or None
            )
        try:
            # 解释器运行的是模型生成的代码，所以机器始终隔离
            machine = await self.client.machines.create(
                self._machine_name(),
                org=settings.BOXD_ORG or None,
                isolated=True,
                labels={"app": "mathmodelagent", "run": self._run_label},
                # 长时间纯计算没有网络流量，不能被待机打断
                auto_suspend_timeout=0,
                # 到期后无论机器处于什么状态都会被删除，任务异常中断时不遗留机器
                delete_after=settings.BOXD_DELETE_AFTER or None,
            )
            self.machine_id = machine.id
            logger.info(f"boxd 机器已创建: {machine.name} ({machine.id})")
            await self.client.machines.wait_until_ready(machine.id)
            await self._setup_kernel()
            await self._upload_all_files()
            await self._pre_execute_code()
            logger.info("boxd 解释器初始化成功")
        except Exception as e:
            logger.error(f"初始化 boxd 解释器失败: {str(e)}")
            if self.machine_id is None:
                await self._find_created_machine()
            # 初始化失败时工作流拿不到解释器，也就不会调用 cleanup，这里删除机器
            await self.cleanup(sync_files=False)
            raise

    async def _find_created_machine(self):
        """创建请求出错（如超时）但机器可能已建好时，按本实例的标签找回它的 ID。"""
        assert self.client is not None
        try:
            machines = await self.client.machines.list(
                org=settings.BOXD_ORG or None, labels={"run": self._run_label}
            )
        except Exception as e:
            logger.warning(f"查询 boxd 机器失败: {str(e)}")
            return
        for machine in machines:
            if machine.name == self._machine_name():
                self.machine_id = machine.id
                logger.warning(f"创建请求出错但机器已建好: {machine.id}")
                return

    async def _run(self, command: str | list[str], timeout: float | None = None):
        """在机器中执行命令。

        Args:
            command: 字符串按 shell 脚本执行（登录 shell，可找到 uv）；
                列表按参数直接执行，不经过 shell。
            timeout: 超时时间（秒），None 表示不限制。

        Returns:
            boxd ExecResult。
        """
        assert self.client is not None and self.machine_id is not None
        argv = ["bash", "-lc", command] if isinstance(command, str) else command
        return await self.client.machines.exec(self.machine_id, argv, timeout=timeout)

    async def _setup_kernel(self):
        """安装内核依赖、上传执行脚本并在后台启动 Jupyter 内核。

        Raises:
            RuntimeError: 环境准备或内核启动失败时抛出。
        """
        assert self.client is not None and self.machine_id is not None
        packages = " ".join(KERNEL_PACKAGES)
        install = (
            "set -e\n"
            f"mkdir -p {REMOTE_WORK_DIR} {REMOTE_HOME}/cells\n"
            f"if [ ! -x {REMOTE_PYTHON} ]; then uv venv -q {REMOTE_HOME}/venv; fi\n"
            f"uv pip install -q --python {REMOTE_PYTHON} {packages}\n"
        )
        result = await self._run(install, timeout=900)
        if result.exit_code != 0:
            raise RuntimeError(f"安装内核依赖失败: {result.stderr[-2000:]}")

        await self.client.machines.files.upload(
            self.machine_id, REMOTE_RUNNER, RUNNER_SOURCE.read_text(encoding="utf-8")
        )
        await self._start_kernel()

    async def _start_kernel(self):
        """在后台启动常驻内核，等待连接文件生成。

        Raises:
            RuntimeError: 内核未能启动时抛出。
        """
        # setsid + nohup 让内核脱离本次 exec，在后续调用之间保持运行
        # 重启时先结束上一个内核及其子进程，卡住的代码不会继续占用机器
        start = (
            f"if [ -s {REMOTE_KERNEL_PID_FILE} ]; then\n"
            f"  kill -9 -- -$(cat {REMOTE_KERNEL_PID_FILE}) 2>/dev/null\n"
            "fi\n"
            f"rm -f {REMOTE_CONNECTION_FILE}\n"
            f"cd {REMOTE_WORK_DIR}\n"
            "PYTHONIOENCODING=utf-8 PYTHONUTF8=1 "
            f"setsid nohup {REMOTE_PYTHON} -m ipykernel_launcher "
            f"-f {REMOTE_CONNECTION_FILE} > {REMOTE_HOME}/kernel.log 2>&1 < /dev/null &\n"
            f"echo $! > {REMOTE_KERNEL_PID_FILE}\n"
            "for i in $(seq 150); do\n"
            f"  [ -s {REMOTE_CONNECTION_FILE} ] && exit 0\n"
            "  sleep 0.2\n"
            "done\n"
            f"cat {REMOTE_HOME}/kernel.log >&2\n"
            "exit 1\n"
        )
        result = await self._run(start, timeout=60)
        if result.exit_code != 0:
            raise RuntimeError(f"启动 Jupyter 内核失败: {result.stderr[-2000:]}")
        logger.info("boxd 机器中的 Jupyter 内核已启动")

    async def _upload_all_files(self):
        """上传工作目录中的数据文件和字体文件到机器"""
        assert self.client is not None and self.machine_id is not None
        logger.info(f"开始上传文件，工作目录: {self.work_dir}")
        if not os.path.exists(self.work_dir):
            raise FileNotFoundError(f"工作目录不存在: {self.work_dir}")

        for file in os.listdir(self.work_dir):
            file_path = os.path.join(self.work_dir, file)
            if not file.endswith(UPLOAD_SUFFIXES) or not os.path.isfile(file_path):
                continue
            with open(file_path, "rb") as f:
                await self.client.machines.files.upload(
                    self.machine_id, f"{REMOTE_WORK_DIR}/{file}", f.read()
                )
            logger.info(f"成功上传文件到 boxd 机器: {file}")

        # 上传的文件本地已有，记录下来避免回传
        listing = await self.client.machines.files.list_dir(
            self.machine_id, REMOTE_WORK_DIR
        )
        for entry in listing.entries:
            if not entry.is_dir:
                self._synced[entry.name] = (entry.size_bytes, entry.modified_at)

    async def _pre_execute_code(self):
        """执行 matplotlib 初始化，并把字体加载结果推送给前端。"""
        init_code = build_matplotlib_init_code(REMOTE_WORK_DIR)
        execution = await self._execute_in_kernel(init_code)
        stdout = "\n".join(text for mark, text in execution if mark == "stdout")
        for line in stdout.splitlines():
            line = line.strip()
            if "中文字体已加载" in line or "未找到中文字体" in line:
                # 去掉日志前缀，前端只展示关键结论
                await redis_manager.publish_message(
                    self.task_id,
                    SystemMessage(
                        content=line.removeprefix("[matplotlib_setup] ").strip(),
                        type="success" if "中文字体已加载" in line else "warning",
                    ),
                )
                return

    async def _execute_in_kernel(self, code: str) -> list[tuple[str, str]]:
        """把代码发送到机器中的内核执行，返回 (类型, 内容) 列表。

        Args:
            code: 待执行的 Python 代码。

        Returns:
            与本地解释器相同格式的输出列表。

        Raises:
            RuntimeError: 内核不可用时抛出。
        """
        assert self.client is not None and self.machine_id is not None
        self._cell_count += 1
        cell_path = f"{REMOTE_HOME}/cells/cell-{self._cell_count}.py"
        cell_timeout = settings.BOXD_CELL_TIMEOUT
        command = [
            REMOTE_PYTHON,
            REMOTE_RUNNER,
            REMOTE_CONNECTION_FILE,
            cell_path,
            str(cell_timeout),
        ]
        try:
            await self.client.machines.files.upload(self.machine_id, cell_path, code)
            # 执行脚本会在超时后中断内核；这里的期限只在它自己也没返回时兜底
            result = await asyncio.wait_for(
                self._run(command),
                cell_timeout + EXEC_GRACE_SECONDS if cell_timeout > 0 else None,
            )
        except asyncio.TimeoutError:
            logger.warning("boxd 执行调用超时未返回，正在重启内核")
            await self._restart_kernel()
            raise KernelRestartedError(
                f"代码执行超过 {cell_timeout} 秒仍未结束，Python 内核已重启，"
                "之前定义的变量和导入已全部丢失，请重新导入库并加载数据，"
                "并把耗时的计算拆小或减小规模后再继续。"
            ) from None
        except ConflictError:
            machine = await self.client.machines.get(self.machine_id)
            if str(machine.status) != "stopped":
                raise
            logger.warning("boxd 机器已停止，正在重新启动并重启内核")
            await self.client.machines.start(self.machine_id)
            await self.client.machines.wait_until_ready(self.machine_id)
            await self._restart_kernel()
            raise KernelRestartedError(
                "代码执行环境曾被停止，现已重新启动，之前定义的变量和导入已全部丢失，"
                "请重新导入库并加载数据后再继续。"
            ) from None

        if result.exit_code in KERNEL_GONE_EXIT_CODES:
            logger.warning(f"boxd 内核不可用: {result.stderr.strip()[-500:]}")
            await self._restart_kernel()
            raise KernelRestartedError(
                "Python 内核已退出（可能内存不足或代码调用了 exit()），现已重启，"
                "之前定义的变量和导入已全部丢失，请重新导入库并加载数据后再继续。"
            )
        if result.exit_code == KERNEL_STUCK_EXIT_CODE:
            logger.warning("boxd 内核超时后不响应中断，正在重启内核")
            await self._restart_kernel()
            raise KernelRestartedError(
                f"代码执行超过 {cell_timeout} 秒且无法中断，Python 内核已重启，"
                "之前定义的变量和导入已全部丢失，请重新导入库并加载数据，"
                "并把耗时的计算拆小或减小规模后再继续。"
            )
        if result.exit_code == CELL_TIMED_OUT_EXIT_CODE:
            logger.warning(f"boxd 代码执行超过 {cell_timeout} 秒，已中断")
            outputs = self._parse_outputs(json.loads(result.stdout))
            # 放在最后，作为返回给代码手的错误信息
            outputs.append(
                (
                    "error",
                    f"代码执行超过 {cell_timeout} 秒，已被中断。之前定义的变量仍然保留，"
                    "请把耗时的计算拆小或减小规模后再继续。",
                )
            )
            return outputs
        if result.exit_code != 0:
            raise RuntimeError(
                f"boxd 内核执行失败 (exit {result.exit_code}): "
                f"{result.stderr.strip()[-2000:]}"
            )
        return self._parse_outputs(json.loads(result.stdout))

    async def _restart_kernel(self):
        """重新启动内核并重新执行 matplotlib 初始化。

        Raises:
            RuntimeError: 重启过程中内核再次不可用时抛出，避免无限重启。
        """
        if self._restarting:
            raise RuntimeError("重启后的 Jupyter 内核仍不可用")
        self._restarting = True
        try:
            await self._start_kernel()
            await self._pre_execute_code()
        finally:
            self._restarting = False

    def _parse_outputs(self, messages: list[dict]) -> list[tuple[str, str]]:
        """将 iopub 消息转换为本地解释器使用的 (类型, 内容) 格式。

        Args:
            messages: 执行脚本返回的 iopub 消息列表。

        Returns:
            (类型, 内容) 列表。
        """
        all_output: list[tuple[str, str]] = []
        for msg in messages:
            msg_type = msg["msg_type"]
            content = msg["content"]
            if msg_type == "stream":
                if content.get("name") == "stdout":
                    all_output.append(("stdout", content["text"]))
            elif msg_type in ("execute_result", "display_data"):
                prefix = "execute_result" if msg_type == "execute_result" else "display"
                data = content.get("data", {})
                if "text/plain" in data:
                    all_output.append((f"{prefix}_text", data["text/plain"]))
                if "text/html" in data:
                    all_output.append((f"{prefix}_html", data["text/html"]))
                if "image/png" in data:
                    all_output.append((f"{prefix}_png", data["image/png"]))
                if "image/jpeg" in data:
                    all_output.append((f"{prefix}_jpeg", data["image/jpeg"]))
            elif msg_type == "error":
                if "traceback" in content:
                    output = "\n".join(content["traceback"])
                    all_output.append(("error", self.delete_color_control_char(output)))
        return all_output

    async def execute_code(self, code: str) -> tuple[str, bool, str]:
        """执行代码并返回结果"""
        if not self.machine_id:
            raise RuntimeError("boxd 机器未初始化")

        logger.info(f"执行代码: {code}")
        self.notebook_serializer.add_code_cell_to_notebook(code)

        text_to_gpt: list[str] = []
        content_to_display: list[OutputItem] | None = []
        error_occurred: bool = False
        error_message: str = ""

        await redis_manager.publish_message(
            self.task_id,
            SystemMessage(content="开始执行代码"),
        )
        logger.info("开始在 boxd 机器中执行代码...")
        try:
            execution = await self._execute_in_kernel(code)
        except Exception as e:
            # 以执行错误的形式返回给代码手，而不是抛出异常打断对话
            message = (
                str(e)
                if isinstance(e, KernelRestartedError)
                else (f"代码执行环境出错: {str(e)}")
            )
            logger.error(message)
            self.notebook_serializer.add_code_cell_error_to_notebook(message)
            await self._push_to_websocket([StdErrModel(msg=message)])
            return message, True, message
        logger.info("代码执行完成，开始处理结果...")

        await redis_manager.publish_message(
            self.task_id,
            SystemMessage(content="代码执行完成"),
        )

        for mark, out_str in execution:
            if mark in ("stdout", "execute_result_text", "display_text"):
                text_to_gpt.append(self._truncate_text(f"[{mark}]\n{out_str}"))
                content_to_display.append(
                    ResultModel(res_type="result", format="text", msg=out_str)
                )
                self.notebook_serializer.add_code_cell_output_to_notebook(out_str)

            elif mark in (
                "execute_result_png",
                "execute_result_jpeg",
                "display_png",
                "display_jpeg",
            ):
                text_to_gpt.append(f"[{mark} 图片已生成，内容为 base64，未展示]")
                if "png" in mark:
                    self.notebook_serializer.add_image_to_notebook(out_str, "image/png")
                    content_to_display.append(
                        ResultModel(res_type="result", format="png", msg=out_str)
                    )
                else:
                    self.notebook_serializer.add_image_to_notebook(
                        out_str, "image/jpeg"
                    )
                    content_to_display.append(
                        ResultModel(res_type="result", format="jpeg", msg=out_str)
                    )

            elif mark == "error":
                error_occurred = True
                error_message = self._truncate_text(out_str)
                logger.error(f"执行错误: {error_message}")
                text_to_gpt.append(error_message)
                self.notebook_serializer.add_code_cell_error_to_notebook(out_str)
                content_to_display.append(StdErrModel(msg=out_str))

        logger.info(f"text_to_gpt: {text_to_gpt}")
        combined_text = "\n".join(text_to_gpt)

        # 代码生成的图片和结果文件同步回本地，供论文手引用
        try:
            await self.download_all_files_from_sandbox()
        except Exception as e:
            logger.error(f"文件同步失败: {str(e)}")

        await self._push_to_websocket(content_to_display)

        return (
            combined_text,
            error_occurred,
            error_message,
        )

    async def download_all_files_from_sandbox(self) -> None:
        """把机器工作目录中新增或修改的文件下载到本地工作目录"""
        assert self.client is not None and self.machine_id is not None
        listing = await self.client.machines.files.list_dir(
            self.machine_id, REMOTE_WORK_DIR
        )
        if listing.truncated:
            logger.warning("boxd 工作目录文件过多，本次只同步了部分文件")
        os.makedirs(self.work_dir, exist_ok=True)
        for entry in listing.entries:
            if entry.is_dir:
                continue
            stamp = (entry.size_bytes, entry.modified_at)
            if self._synced.get(entry.name) == stamp:
                continue
            try:
                content = await self.client.machines.files.download(
                    self.machine_id, f"{REMOTE_WORK_DIR}/{entry.name}"
                )
                with open(os.path.join(self.work_dir, entry.name), "wb") as f:
                    f.write(content)
                self._synced[entry.name] = stamp
                logger.info(f"同步文件: {entry.name}")
            except Exception as e:
                logger.error(f"同步文件 {entry.name} 失败: {str(e)}")

    async def get_created_images(self, section: str) -> list[str]:
        """获取新创建的图片列表（文件已同步到本地工作目录）"""
        current_images = {
            file for file in os.listdir(self.work_dir) if file.endswith(IMAGE_SUFFIXES)
        }
        new_images = current_images - self.last_created_images
        self.last_created_images = current_images
        logger.info(f"{section}-新创建的图片列表: {new_images}")
        return list(new_images)

    async def cleanup(self, sync_files: bool = True):
        """同步文件后删除本任务创建的机器。

        Args:
            sync_files: 删除前是否把机器中的文件同步到本地。初始化失败时
                机器里还没有结果文件，直接删除。
        """
        if not self.client:
            return
        if self.machine_id:
            if sync_files:
                try:
                    await self.download_all_files_from_sandbox()
                except Exception as e:
                    logger.error(f"下载文件失败: {str(e)}")
            try:
                await self.client.machines.delete(self.machine_id)
                logger.info(f"已删除 boxd 机器: {self.machine_id}")
                self.machine_id = None
            except Exception as e:
                logger.error(f"删除 boxd 机器失败: {str(e)}")
        if self._owns_client:
            await self.client.close()
            self.client = None
