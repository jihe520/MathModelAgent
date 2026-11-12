"""在 boxd 机器内运行的单元执行脚本。

BoxdCodeInterpreter 会把本文件上传到机器里，每次执行代码时调用一次：
连接常驻的 Jupyter 内核，执行一个代码文件，把 iopub 输出以 JSON 打印到 stdout。
内核本身常驻后台，因此变量在多次执行之间保留。

用法：python boxd_kernel_runner.py <connection_file> <cell_file> [timeout_seconds]
"""

import json
import queue
import sys
import time

from jupyter_client.blocking.client import BlockingKernelClient

# 长时间无输出时定期向 stderr 写一个字节，避免连接因静默而被中间层断开
KEEPALIVE_SECONDS = 30
# 发出中断后等待内核停下来的时间
INTERRUPT_GRACE_SECONDS = 10
# 退出码：3 内核未就绪，4 内核在执行中退出，5 超时后已中断（变量保留），6 超时且中断无效
EXIT_NOT_READY = 3
EXIT_KERNEL_DIED = 4
EXIT_TIMED_OUT = 5
EXIT_STUCK = 6


def main(connection_file: str, cell_file: str, timeout: float = 0) -> int:
    """执行一个代码文件并打印其输出。

    Args:
        connection_file: 内核连接文件路径。
        cell_file: 待执行的代码文件路径。
        timeout: 单次执行的时间上限（秒），0 表示不限制。超时后中断内核，
            已产生的输出照常打印。

    Returns:
        进程退出码，0 表示内核正常返回（代码本身报错也算正常返回）。
    """
    kc = BlockingKernelClient(connection_file=connection_file)
    kc.load_connection_file()
    kc.start_channels()
    try:
        kc.wait_for_ready(timeout=60)
    except RuntimeError as e:
        print(f"内核未就绪: {e}", file=sys.stderr)
        return EXIT_NOT_READY

    with open(cell_file, encoding="utf-8") as f:
        code = f.read()
    # 没有前端可以响应 input()，关闭 stdin 避免代码卡住
    msg_id = kc.execute(code, allow_stdin=False)

    outputs = []
    # deadline 先是执行的时间上限；中断发出后改为等待内核停下的期限
    deadline = time.monotonic() + timeout if timeout > 0 else None
    interrupted = False
    while True:
        # 每轮都检查期限：不停打印输出的代码同样会超时
        if deadline is not None and time.monotonic() >= deadline:
            if interrupted:
                print("内核没有响应中断", file=sys.stderr)
                return EXIT_STUCK
            # 走 Jupyter 协议的中断请求，内核保持运行，变量不丢
            kc.control_channel.send(kc.session.msg("interrupt_request", {}))
            interrupted = True
            deadline = time.monotonic() + INTERRUPT_GRACE_SECONDS
        wait = KEEPALIVE_SECONDS
        if deadline is not None:
            wait = min(wait, max(deadline - time.monotonic(), 0))
        try:
            msg = kc.get_iopub_msg(timeout=wait)
        except queue.Empty:
            if not kc.is_alive():
                print("内核已退出", file=sys.stderr)
                return EXIT_KERNEL_DIED
            if deadline is None or time.monotonic() < deadline:
                sys.stderr.write(" ")
                sys.stderr.flush()
            continue
        if msg["parent_header"].get("msg_id") != msg_id:
            continue
        msg_type = msg["msg_type"]
        content = msg["content"]
        if msg_type == "status" and content.get("execution_state") == "idle":
            break
        if msg_type in ("stream", "execute_result", "display_data", "error"):
            outputs.append({"msg_type": msg_type, "content": content})

    kc.stop_channels()
    print(json.dumps(outputs))
    return EXIT_TIMED_OUT if interrupted else 0


if __name__ == "__main__":
    limit = float(sys.argv[3]) if len(sys.argv) > 3 else 0
    sys.exit(main(sys.argv[1], sys.argv[2], limit))
