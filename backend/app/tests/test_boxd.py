"""boxd 代码解释器测试：用假客户端测试单元行为，配置 BOXD_API_KEY 时运行真实机器测试。"""

import asyncio
import contextlib
import io
import json
import os
import shutil
import tempfile
import unittest
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

from boxd.errors import ConflictError
from jupyter_client.manager import KernelManager

from app.config.setting import settings
from app.tools import boxd_interpreter, boxd_kernel_runner
from app.tools.boxd_interpreter import (
    REMOTE_RUNNER,
    REMOTE_WORK_DIR,
    BoxdCodeInterpreter,
)
from app.tools.notebook_serializer import NotebookSerializer

T0 = datetime(2026, 1, 1, tzinfo=timezone.utc)
T1 = datetime(2026, 1, 1, 0, 1, tzinfo=timezone.utc)


class FakeFiles:
    """记录上传、模拟远端工作目录的文件接口。"""

    def __init__(self):
        self.uploads: dict[str, bytes] = {}
        self.remote: dict[str, tuple[bytes, datetime]] = {}
        self.downloads: list[str] = []

    async def upload(self, machine_id, path, data):
        data = data.encode() if isinstance(data, str) else data
        self.uploads[path] = data
        if path.startswith(REMOTE_WORK_DIR + "/"):
            self.remote[path.rsplit("/", 1)[1]] = (data, T0)
        return len(data)

    async def list_dir(self, machine_id, path):
        entries = [
            SimpleNamespace(
                name=name, is_dir=False, size_bytes=len(data), modified_at=mtime
            )
            for name, (data, mtime) in self.remote.items()
        ]
        return SimpleNamespace(entries=entries, truncated=False)

    async def download(self, machine_id, path):
        self.downloads.append(path)
        return self.remote[path.rsplit("/", 1)[1]][0]


class FakeMachines:
    """模拟 boxd machines 接口，按顺序返回内核执行结果。"""

    def __init__(self):
        self.files = FakeFiles()
        self.create_kwargs: dict = {}
        self.commands: list[str] = []
        self.kernel_outputs: list[list[dict]] = []
        self.argvs: list[list[str]] = []
        self.conflicts = 0
        self.status = "running"
        self.runner_exit_codes: list[int] = []
        self.fail_install = False
        self.create_error: Exception | None = None
        self.hang_runner = False
        self.list_filters: list[dict] = []
        self.started: list[str] = []
        self.deleted: list[str] = []

    async def create(self, name, **kwargs):
        self.create_kwargs = {"name": name, **kwargs}
        if self.create_error:
            # 机器已经建好，但调用方没有拿到响应
            raise self.create_error
        return SimpleNamespace(id="vm-123", name=name)

    async def list(self, org=None, labels=None):
        self.list_filters.append(dict(labels or {}))
        created = self.create_kwargs
        if not created or (labels or {}).items() > created["labels"].items():
            return []
        return [SimpleNamespace(id="vm-123", name=created["name"])]

    async def wait_until_ready(self, machine_id):
        return None

    async def get(self, machine_id):
        return SimpleNamespace(id=machine_id, status=self.status)

    async def start(self, machine_id):
        self.started.append(machine_id)

    async def delete(self, machine_id):
        self.deleted.append(machine_id)

    async def exec(self, machine_id, command, timeout=None):
        assert machine_id == "vm-123", "必须按 id 访问机器"
        self.argvs.append(list(command))
        script = " ".join(command)
        self.commands.append(script)
        if REMOTE_RUNNER in script:
            if self.conflicts:
                self.conflicts -= 1
                raise ConflictError("conflict")
            if self.hang_runner:
                self.hang_runner = False
                await asyncio.sleep(3600)
            if self.runner_exit_codes:
                code = self.runner_exit_codes.pop(0)
                if code == boxd_interpreter.CELL_TIMED_OUT_EXIT_CODE:
                    # 超时被中断的执行仍然打印已产生的输出
                    outputs = self.kernel_outputs.pop(0)
                    return SimpleNamespace(
                        exit_code=code, stdout=json.dumps(outputs), stderr=""
                    )
                return SimpleNamespace(exit_code=code, stdout="", stderr="kernel gone")
            outputs = self.kernel_outputs.pop(0) if self.kernel_outputs else []
            return SimpleNamespace(exit_code=0, stdout=json.dumps(outputs), stderr="")
        if self.fail_install and "uv pip install" in script:
            return SimpleNamespace(exit_code=1, stdout="", stderr="network down")
        return SimpleNamespace(exit_code=0, stdout="", stderr="")


def stdout(text: str) -> dict:
    return {"msg_type": "stream", "content": {"name": "stdout", "text": text}}


class BoxdTestBase(unittest.IsolatedAsyncioTestCase):
    """创建临时工作目录并屏蔽 Redis 消息发布。"""

    def setUp(self):
        self.work_dir = tempfile.mkdtemp()
        self.notebook = NotebookSerializer(self.work_dir)
        patcher = patch.object(
            boxd_interpreter.redis_manager, "publish_message", new=AsyncMock()
        )
        self.publish = patcher.start()
        self.addCleanup(patcher.stop)
        self.addCleanup(shutil.rmtree, self.work_dir, ignore_errors=True)


class TestBoxdCodeInterpreter(BoxdTestBase):
    """BoxdCodeInterpreter 单元测试（假客户端）。"""

    async def asyncSetUp(self):
        self.machines = FakeMachines()
        client = SimpleNamespace(machines=self.machines)
        with open(os.path.join(self.work_dir, "data.csv"), "w") as f:
            f.write("a,b\n1,2\n")
        self.interp = BoxdCodeInterpreter(
            "20250312-104132-D3625CAB",
            self.work_dir,
            self.notebook,
            client=client,  # type: ignore[arg-type]
        )
        self.machines.kernel_outputs.append(
            [stdout("[matplotlib_setup] 中文字体已加载\n")]
        )
        await self.interp.initialize()

    async def test_creates_isolated_machine_without_standby(self):
        kwargs = self.machines.create_kwargs
        self.assertTrue(kwargs["isolated"])
        self.assertEqual(kwargs["auto_suspend_timeout"], 0)
        self.assertEqual(kwargs["delete_after"], settings.BOXD_DELETE_AFTER)
        self.assertNotIn("auto_destroy_timeout", kwargs)
        self.assertEqual(kwargs["name"], "mathmodelagent-20250312-104132-d3625cab")
        self.assertEqual(kwargs["labels"]["app"], "mathmodelagent")
        self.assertEqual(self.interp.machine_id, "vm-123")

    async def test_starts_kernel_and_uploads_data(self):
        self.assertIn(REMOTE_RUNNER, self.machines.files.uploads)
        self.assertIn(f"{REMOTE_WORK_DIR}/data.csv", self.machines.files.uploads)
        self.assertTrue(any("ipykernel_launcher" in c for c in self.machines.commands))
        self.assertTrue(any("setsid nohup" in c for c in self.machines.commands))
        # 字体加载结果推送给前端
        sent = [call.args[1].content for call in self.publish.await_args_list]
        self.assertIn("中文字体已加载", sent)

    async def test_execute_code_returns_stdout_and_errors(self):
        self.machines.kernel_outputs.append(
            [
                stdout("hi 42\n"),
                {
                    "msg_type": "error",
                    "content": {"traceback": ["\x1b[31mZeroDivisionError\x1b[0m"]},
                },
            ]
        )
        text, failed, error = await self.interp.execute_code("print('hi', 42); 1/0")
        self.assertIn("hi 42", text)
        self.assertTrue(failed)
        self.assertEqual(error, "ZeroDivisionError")

    async def test_execute_code_reports_images(self):
        self.machines.kernel_outputs.append(
            [{"msg_type": "display_data", "content": {"data": {"image/png": "iVBOR"}}}]
        )
        text, failed, _ = await self.interp.execute_code("plt.show()")
        self.assertFalse(failed)
        self.assertIn("display_png", text)

    async def test_syncs_new_files_but_not_uploaded_ones(self):
        self.machines.files.remote["fig1.png"] = (b"png-bytes", T1)
        await self.interp.execute_code("plt.savefig('fig1.png')")
        with open(os.path.join(self.work_dir, "fig1.png"), "rb") as f:
            self.assertEqual(f.read(), b"png-bytes")
        self.assertEqual(self.machines.files.downloads, [f"{REMOTE_WORK_DIR}/fig1.png"])
        self.assertEqual(await self.interp.get_created_images("q1"), ["fig1.png"])
        # 未变化的文件不会重复下载，已报告的图片不会重复报告
        await self.interp.execute_code("pass")
        self.assertEqual(len(self.machines.files.downloads), 1)
        self.assertEqual(await self.interp.get_created_images("q2"), [])

    def kernel_starts(self) -> int:
        return sum("ipykernel_launcher" in c for c in self.machines.commands)

    async def test_runner_runs_without_a_shell(self):
        runner_argv = [a for a in self.machines.argvs if REMOTE_RUNNER in a]
        self.assertTrue(runner_argv)
        self.assertNotEqual(runner_argv[0][0], "bash")

    async def test_starts_stopped_machine_and_restarts_kernel(self):
        self.machines.conflicts = 1
        self.machines.status = "stopped"
        text, failed, error = await self.interp.execute_code("print(df)")
        self.assertEqual(self.machines.started, ["vm-123"])
        self.assertEqual(self.kernel_starts(), 2)
        # 告诉代码手变量已丢失，而不是抛出异常
        self.assertTrue(failed)
        self.assertIn("变量", error)

    async def test_conflict_on_running_machine_is_reported_not_restarted(self):
        self.machines.conflicts = 1
        _, failed, error = await self.interp.execute_code("print(1)")
        self.assertTrue(failed)
        self.assertIn("代码执行环境出错", error)
        self.assertEqual(self.machines.started, [])
        self.assertEqual(self.kernel_starts(), 1)

    async def test_dead_kernel_is_restarted_and_reported(self):
        self.machines.runner_exit_codes.append(4)
        _, failed, error = await self.interp.execute_code("exit()")
        self.assertTrue(failed)
        self.assertIn("内核已退出", error)
        self.assertEqual(self.kernel_starts(), 2)
        # 重启后可以继续执行
        self.machines.kernel_outputs.append([stdout("back\n")])
        text, failed, _ = await self.interp.execute_code("print('back')")
        self.assertIn("back", text)
        self.assertFalse(failed)

    async def test_runner_gets_the_cell_timeout(self):
        runner_argv = [a for a in self.machines.argvs if REMOTE_RUNNER in a]
        self.assertEqual(runner_argv[0][-1], str(settings.BOXD_CELL_TIMEOUT))
        self.assertGreater(settings.BOXD_CELL_TIMEOUT, 0)

    async def test_timed_out_cell_is_reported_and_kernel_kept(self):
        self.machines.runner_exit_codes.append(5)
        self.machines.kernel_outputs.append([stdout("step 1 done\n")])
        text, failed, error = await self.interp.execute_code("while True: pass")
        self.assertTrue(failed)
        self.assertIn(f"超过 {settings.BOXD_CELL_TIMEOUT} 秒", error)
        self.assertIn("变量仍然保留", error)
        # 超时前的输出仍然返回，内核没有重启
        self.assertIn("step 1 done", text)
        self.assertEqual(self.kernel_starts(), 1)

    async def test_cell_that_ignores_interrupt_restarts_kernel(self):
        self.machines.runner_exit_codes.append(6)
        _, failed, error = await self.interp.execute_code("stuck()")
        self.assertTrue(failed)
        self.assertIn("无法中断", error)
        self.assertIn("全部丢失", error)
        self.assertEqual(self.kernel_starts(), 2)
        # 重启前结束上一个内核
        self.assertIn("kill -9", self.machines.commands[-2])

    async def test_exec_that_never_returns_is_cut_off(self):
        self.machines.hang_runner = True
        with (
            patch.object(settings, "BOXD_CELL_TIMEOUT", 1),
            patch.object(boxd_interpreter, "EXEC_GRACE_SECONDS", -0.95),
        ):
            _, failed, error = await asyncio.wait_for(
                self.interp.execute_code("stuck()"), 5
            )
        self.assertTrue(failed)
        self.assertIn("全部丢失", error)
        self.assertEqual(self.kernel_starts(), 2)

    async def test_delete_after_zero_sets_no_timer(self):
        machines = FakeMachines()
        interp = BoxdCodeInterpreter(
            "task",
            self.work_dir,
            self.notebook,
            client=SimpleNamespace(machines=machines),  # type: ignore[arg-type]
        )
        with patch.object(settings, "BOXD_DELETE_AFTER", 0):
            await interp.initialize()
        self.assertIsNone(machines.create_kwargs["delete_after"])

    async def test_cleanup_deletes_machine_by_id(self):
        await self.interp.cleanup()
        self.assertEqual(self.machines.deleted, ["vm-123"])
        self.assertIsNone(self.interp.machine_id)


class TestBoxdInitFailure(BoxdTestBase):
    """初始化失败时删除已创建的机器。"""

    async def test_failed_setup_deletes_machine(self):
        machines = FakeMachines()
        machines.fail_install = True
        interp = BoxdCodeInterpreter(
            "task",
            self.work_dir,
            self.notebook,
            client=SimpleNamespace(machines=machines),  # type: ignore[arg-type]
        )
        with self.assertRaisesRegex(RuntimeError, "安装内核依赖失败"):
            await interp.initialize()
        self.assertEqual(machines.deleted, ["vm-123"])

    async def test_create_that_fails_after_the_machine_exists_deletes_it(self):
        machines = FakeMachines()
        machines.create_error = TimeoutError("create timed out")
        interp = BoxdCodeInterpreter(
            "task",
            self.work_dir,
            self.notebook,
            client=SimpleNamespace(machines=machines),  # type: ignore[arg-type]
        )
        with self.assertRaisesRegex(TimeoutError, "create timed out"):
            await interp.initialize()
        # 只按本实例独有的标签查找，不会碰到别的机器
        self.assertEqual(
            machines.list_filters, [{"run": machines.create_kwargs["labels"]["run"]}]
        )
        self.assertEqual(machines.deleted, ["vm-123"])
        self.assertEqual(machines.files.downloads, [])


class TestKernelRunner(unittest.TestCase):
    """执行脚本的超时行为（本地启动一个真实内核）。"""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.dir, ignore_errors=True)
        self.km = KernelManager()
        self.km.start_kernel()
        self.addCleanup(self.km.shutdown_kernel, now=True)

    def run_cell(self, code: str, timeout: float = 0) -> tuple[int, list[dict]]:
        cell = os.path.join(self.dir, "cell.py")
        with open(cell, "w", encoding="utf-8") as f:
            f.write(code)
        out = io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(io.StringIO()):
            code_ = boxd_kernel_runner.main(self.km.connection_file, cell, timeout)
        return code_, json.loads(out.getvalue() or "[]")

    def test_stuck_cell_is_interrupted_and_state_kept(self):
        self.assertEqual(self.run_cell("x = 41")[0], 0)
        exit_code, outputs = self.run_cell(
            "import time\nprint('before', flush=True)\ntime.sleep(600)", timeout=1
        )
        self.assertEqual(exit_code, boxd_kernel_runner.EXIT_TIMED_OUT)
        self.assertEqual(outputs[0]["content"]["text"], "before\n")
        self.assertEqual(outputs[-1]["content"]["ename"], "KeyboardInterrupt")
        # 内核还在，变量保留
        exit_code, outputs = self.run_cell("print(x + 1)")
        self.assertEqual(exit_code, 0)
        self.assertEqual(outputs[0]["content"]["text"], "42\n")

    def test_chatty_cell_is_interrupted_too(self):
        exit_code, _ = self.run_cell(
            "import time\nwhile True:\n    print('.')\n    time.sleep(0.01)", timeout=1
        )
        self.assertEqual(exit_code, boxd_kernel_runner.EXIT_TIMED_OUT)


class TestBoxdMissingKey(BoxdTestBase):
    """未配置密钥时给出明确错误。"""

    async def test_missing_api_key_raises(self):
        interp = BoxdCodeInterpreter("task", self.work_dir, self.notebook)
        with patch.object(settings, "BOXD_API_KEY", None):
            with self.assertRaisesRegex(ValueError, "BOXD_API_KEY"):
                await interp.initialize()


@unittest.skipUnless(os.getenv("BOXD_API_KEY"), "BOXD_API_KEY not set")
class TestBoxdLive(BoxdTestBase):
    """在真实 boxd 机器上运行（需要 BOXD_API_KEY，会创建并删除一台机器）。"""

    async def test_execute_code_end_to_end(self):
        prefix = os.getenv("BOXD_TEST_NAME_PREFIX", "mathmodelagent-test-")
        with open(os.path.join(self.work_dir, "data.csv"), "w") as f:
            f.write("x,y\n1,2\n2,4\n3,6\n")
        with patch.object(settings, "BOXD_API_KEY", os.environ["BOXD_API_KEY"]):
            interp = BoxdCodeInterpreter(
                f"live-{os.getpid()}", self.work_dir, self.notebook, name_prefix=prefix
            )
            await interp.initialize()
        try:
            text, failed, _ = await interp.execute_code(
                "import pandas as pd\ndf = pd.read_csv('data.csv')\nprint(df.y.sum())"
            )
            self.assertFalse(failed, text)
            self.assertIn("12", text)

            # 变量在多次执行之间保留
            text, failed, _ = await interp.execute_code("print(len(df))")
            self.assertIn("3", text)

            text, failed, _ = await interp.execute_code(
                "import matplotlib.pyplot as plt\n"
                "plt.plot(df.x, df.y)\nplt.savefig('fig.png')\nplt.show()"
            )
            self.assertFalse(failed, text)
            self.assertIn("png", text)
            self.assertIn("fig.png", await interp.get_created_images("q1"))
            self.assertTrue(os.path.exists(os.path.join(self.work_dir, "fig.png")))

            _, failed, error = await interp.execute_code("1/0")
            self.assertTrue(failed)
            self.assertIn("ZeroDivisionError", error)

            # 超时的执行被中断，变量保留
            with patch.object(settings, "BOXD_CELL_TIMEOUT", 5):
                _, failed, error = await interp.execute_code(
                    "import time\ntime.sleep(600)"
                )
            self.assertTrue(failed)
            self.assertIn("超过 5 秒", error)
            text, failed, _ = await interp.execute_code("print(len(df))")
            self.assertFalse(failed, text)
            self.assertIn("3", text)
        finally:
            machine_id = interp.machine_id
            await interp.cleanup()
        self.assertIsNone(interp.machine_id)
        print(f"live machine {machine_id} deleted by cleanup()")


if __name__ == "__main__":
    unittest.main()
