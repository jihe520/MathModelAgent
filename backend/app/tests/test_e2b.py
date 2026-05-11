"""E2B 代码解释器集成测试。"""

import os
import asyncio
import unittest

from app.tools.e2b_interpreter import E2BCodeInterpreter
from app.tools.notebook_serializer import NotebookSerializer
from app.utils.common_utils import create_work_dir



class TestE2BCodeInterpreter(unittest.TestCase):
    """E2B 代码解释器测试用例。"""

    def setUp(self):
        """初始化测试环境，创建沙箱和代码解释器。"""
        if E2BCodeInterpreter is None:
            self.skipTest("e2b_code_interpreter not available")
        self.task_id = "20250312-104132-d3625cab"
        self.work_dir = create_work_dir(self.task_id)
        notebook_path = os.path.join(self.work_dir, "jupyter")
        notebook = NotebookSerializer(notebook_path)

        self.code_interpreter = E2BCodeInterpreter(
            self.task_id, self.work_dir, notebook
        )

    def test_execute_code(self):
        """测试在 E2B 沙箱中执行 Python 代码。"""
        if not os.getenv("E2B_API_KEY"):
            self.skipTest("E2B_API_KEY not set")

        code = """
import matplotlib.pyplot as plt
import numpy as np

# 生成数据
x = np.linspace(0, 2 * np.pi, 100)  # x从0到2π，生成100个点
y = np.sin(x)                       # 计算对应的sin(x)值

# 绘图
plt.figure(figsize=(8, 4))          # 设置画布大小
plt.plot(x, y, label='y = sin(x)')  # 绘制曲线，并添加图例

# 添加标签和标题
plt.title("Simple Sine Function")
plt.xlabel("x")
plt.ylabel("y")

# 添加网格和图例
plt.grid(True)
plt.legend()

# 显示图像
plt.show()
"""
        asyncio.run(self.code_interpreter.initialize())
        asyncio.run(self.code_interpreter.execute_code(code))

