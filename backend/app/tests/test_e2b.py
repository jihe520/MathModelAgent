import unittest

from dotenv import load_dotenv

from app.tools.e2b_interpreter import E2BCodeInterpreter
from app.utils.common_utils import create_task_id, create_work_dir
from app.utils.notebook_serializer import NotebookSerializer


class TestE2BCodeInterpreter(unittest.TestCase):
    def setUp(self):
        load_dotenv()
        _, dirs = create_work_dir("20250312-104132-d3625cab")
        notebook = NotebookSerializer(dirs["jupyter"])
        self.code_interpreter = E2BCodeInterpreter(
            dirs, "20250312-104132-d3625cab", notebook
        )

    def test_execute_code(self):
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
        self.code_interpreter.execute_code(code)
