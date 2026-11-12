"""在 boxd 机器内运行的单元执行脚本。

BoxdCodeInterpreter 会把本文件上传到机器里，每次执行代码时调用一次：
连接常驻的 Jupyter 内核，执行一个代码文件，把 iopub 输出以 JSON 打印到 stdout。
内核本身常驻后台，因此变量在多次执行之间保留。

用法：python boxd_kernel_runner.py <connection_file> <cell_file>
"""

import json
import queue
import sys

from jupyter_client.blocking.client import BlockingKernelClient

# 长时间无输出时定期向 stderr 写一个字节，避免连接因静默而被中间层断开
KEEPALIVE_SECONDS = 30


def main(connection_file: str, cell_file: str) -> int:
    """执行一个代码文件并打印其输出。

    Args:
        connection_file: 内核连接文件路径。
        cell_file: 待执行的代码文件路径。

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
        return 3

    with open(cell_file, encoding="utf-8") as f:
        code = f.read()
    # 没有前端可以响应 input()，关闭 stdin 避免代码卡住
    msg_id = kc.execute(code, allow_stdin=False)

    outputs = []
    while True:
        try:
            msg = kc.get_iopub_msg(timeout=KEEPALIVE_SECONDS)
        except queue.Empty:
            if not kc.is_alive():
                print("内核已退出", file=sys.stderr)
                return 4
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
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
