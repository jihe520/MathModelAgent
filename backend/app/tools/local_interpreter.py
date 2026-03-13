from app.tools.base_interpreter import BaseCodeInterpreter
from app.tools.notebook_serializer import NotebookSerializer
import jupyter_client
from app.utils.log_util import logger
import os
from app.services.redis_manager import redis_manager
from app.schemas.response import (
    OutputItem,
    ResultModel,
    StdErrModel,
    SystemMessage,
)


class LocalCodeInterpreter(BaseCodeInterpreter):
    def __init__(
        self,
        task_id: str,
        work_dir: str,
        notebook_serializer: NotebookSerializer,
    ):
        super().__init__(task_id, work_dir, notebook_serializer)
        self.km, self.kc = None, None
        self.interrupt_signal = False

    async def initialize(self):
        # 本地内核一般不需异步上传文件，直接切换目录即可
        # 初始化 Jupyter 内核管理器和客户端
        logger.info("初始化本地内核")
        self.km, self.kc = jupyter_client.manager.start_new_kernel(
            kernel_name="python3"
        )
        self._pre_execute_code()

    def _pre_execute_code(self):
        # 获取安全工具代码
        safe_tools_code = self._get_safe_tools_code()
        
        init_code = (
            f"import os\n"
            f"work_dir = r'{self.work_dir}'\n"
            f"os.makedirs(work_dir, exist_ok=True)\n"
            f"os.chdir(work_dir)\n"
            f"print('当前工作目录:', os.getcwd())\n"
            f"import matplotlib.pyplot as plt\n"
            f"import matplotlib as mpl\n"
            f"# 配置中文字体支持\n"
            f"plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS', 'WenQuanYi Micro Hei', 'PingFang SC', 'Hiragino Sans GB', 'Heiti SC', 'DejaVu Sans', 'sans-serif']\n"
            f"plt.rcParams['axes.unicode_minus'] = False\n"
            f"plt.rcParams['font.family'] = 'sans-serif'\n"
            f"mpl.rcParams['font.size'] = 12\n"
            f"mpl.rcParams['axes.labelsize'] = 12\n"
            f"mpl.rcParams['xtick.labelsize'] = 10\n"
            f"mpl.rcParams['ytick.labelsize'] = 10\n"
            f"# 设置DPI以获得更清晰的显示\n"
            f"mpl.rcParams['figure.dpi'] = 100\n"
            f"mpl.rcParams['savefig.dpi'] = 300\n"
            f"print('✓ 中文字体配置完成')\n"
            f"\n# 注入安全数据处理工具\n"
            f"{safe_tools_code}\n"
            f"print('✓ 安全数据处理工具已加载')\n"
        )
        self.execute_code_(init_code)
    
    def _get_safe_tools_code(self):
        """获取安全数据处理工具的代码"""
        return '''
# 通用安全数据处理工具
import pandas as pd
from typing import List, Optional, Any, Dict

class SafeDataProcessor:
    """安全的数据处理工具类，适用于任意数据集"""
    
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.column_info = self._analyze_columns()
        
    def _analyze_columns(self) -> Dict[str, List[str]]:
        """分析数据集的列结构"""
        info = {
            'numeric_cols': [],
            'categorical_cols': [],
            'datetime_cols': [],
            'text_cols': []
        }
        
        for col in self.df.columns:
            dtype = str(self.df[col].dtype)
            if 'int' in dtype or 'float' in dtype:
                info['numeric_cols'].append(col)
            elif 'datetime' in dtype:
                info['datetime_cols'].append(col)
            elif self.df[col].dtype == 'object':
                # 判断是分类变量还是文本变量
                unique_ratio = self.df[col].nunique() / len(self.df)
                if unique_ratio < 0.5:  # 唯一值比例小于50%认为是分类变量
                    info['categorical_cols'].append(col)
                else:
                    info['text_cols'].append(col)
            else:
                info['categorical_cols'].append(col)
                
        return info
    
    def safe_get_column(self, 
                       possible_names: List[str], 
                       description: str = "目标列",
                       fuzzy_match: bool = True) -> Optional[str]:
        """安全获取列名，支持精确匹配和模糊匹配"""
        # 精确匹配
        for name in possible_names:
            if name in self.df.columns:
                print(f"找到{description}的精确匹配: {name}")
                return name
        
        if fuzzy_match:
            # 模糊匹配
            for keyword in possible_names:
                matches = [col for col in self.df.columns if keyword in col]
                if matches:
                    print(f"找到{description}的模糊匹配: {matches[0]} (关键词: {keyword})")
                    return matches[0]
        
        print(f"警告: 未找到{description}列，尝试的名称: {possible_names}")
        print(f"可用列名: {self.df.columns.tolist()}")
        return None
    
    def safe_get_numeric_columns(self) -> List[str]:
        """获取所有数值型列"""
        return self.column_info['numeric_cols']
    
    def safe_get_categorical_columns(self) -> List[str]:
        """获取所有分类型列"""
        return self.column_info['categorical_cols']
    
    def safe_select_columns(self, column_names: List[str]) -> pd.DataFrame:
        """安全选择列，自动过滤不存在的列名"""
        existing_cols = [col for col in column_names if col in self.df.columns]
        missing_cols = [col for col in column_names if col not in self.df.columns]
        
        if missing_cols:
            print(f"以下列不存在，已自动跳过: {missing_cols}")
        
        if existing_cols:
            print(f"成功选择列: {existing_cols}")
            return self.df[existing_cols]
        else:
            print("错误: 没有找到任何指定的列")
            return pd.DataFrame()
    
    def print_data_summary(self):
        """打印数据集摘要信息"""
        print("=" * 50)
        print("数据集基本信息")
        print("=" * 50)
        print(f"数据形状: {self.df.shape}")
        print(f"总列数: {len(self.df.columns)}")
        print(f"数值型列数: {len(self.column_info['numeric_cols'])}")
        print(f"分类型列数: {len(self.column_info['categorical_cols'])}")
        print(f"日期型列数: {len(self.column_info['datetime_cols'])}")
        print(f"文本型列数: {len(self.column_info['text_cols'])}")
        
        print("\\n列名列表:")
        for i, col in enumerate(self.df.columns, 1):
            print(f"  {i:2d}. {col} ({self.df[col].dtype})")
        
        print(f"\\n缺失值统计:")
        missing_info = self.df.isnull().sum()
        missing_cols = missing_info[missing_info > 0]
        if len(missing_cols) > 0:
            print(missing_cols)
        else:
            print("无缺失值")
            
        print(f"\\n前5行数据:")
        print(self.df.head())
    
    def auto_detect_target_column(self) -> Optional[str]:
        """自动检测可能的目标变量列"""
        target_patterns = [
            'label', 'target', '标签', '目标', '类别', '分类',
            'class', 'category', 'type', '类型', '结果', 'result',
            '行为特征', '特征', '状态', 'status'
        ]
        
        for pattern in target_patterns:
            matched_col = self.safe_get_column([pattern], "目标变量", fuzzy_match=True)
            if matched_col:
                return matched_col
        
        # 如果找不到，返回最后一列
        if len(self.df.columns) > 0:
            last_col = self.df.columns[-1]
            print(f"未找到明确的目标列，使用最后一列作为目标: {last_col}")
            return last_col
        
        return None

# 通用安全数据加载函数
def safe_load_data(file_path: str):
    """通用安全数据加载函数，自动处理各种格式和编码"""
    try:
        if file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            # 尝试不同编码
            for encoding in ['utf-8', 'gbk', 'gb2312', 'latin1']:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    print(f"使用编码 {encoding} 成功加载数据")
                    break
                except (UnicodeDecodeError, UnicodeError):
                    continue
            else:
                raise ValueError("无法使用常见编码解码CSV文件")
        else:
            # 默认尝试CSV
            df = pd.read_csv(file_path)
        
        print(f"数据加载成功！形状: {df.shape}")
        return df
        
    except Exception as e:
        print(f"数据加载失败: {e}")
        print(f"请检查文件路径: {file_path}")
        return None

# 使用便捷函数
def quick_data_analysis(file_path: str):
    """快速数据分析函数"""
    df = safe_load_data(file_path)
    if df is not None:
        processor = SafeDataProcessor(df)
        processor.print_data_summary()
        return df, processor
    return None, None
'''

    async def execute_code(self, code: str) -> tuple[str, bool, str]:
        logger.info(f"执行代码: {code}")
        #  添加代码到notebook
        self.notebook_serializer.add_code_cell_to_notebook(code)

        text_to_gpt: list[str] = []
        content_to_display: list[OutputItem] | None = []
        error_occurred: bool = False
        error_message: str = ""

        await redis_manager.publish_message(
            self.task_id,
            SystemMessage(content="开始执行代码"),
        )
        # 执行 Python 代码
        logger.info("开始在本地执行代码...")
        execution = self.execute_code_(code)
        logger.info("代码执行完成，开始处理结果...")

        await redis_manager.publish_message(
            self.task_id,
            SystemMessage(content="代码执行完成"),
        )

        for mark, out_str in execution:
            if mark in ("stdout", "execute_result_text", "display_text"):
                text_to_gpt.append(self._truncate_text(f"[{mark}]\n{out_str}"))
                #  添加text到notebook
                content_to_display.append(
                    ResultModel(type="result", format="text", msg=out_str)
                )
                self.notebook_serializer.add_code_cell_output_to_notebook(out_str)

            elif mark in (
                "execute_result_png",
                "execute_result_jpeg",
                "display_png",
                "display_jpeg",
            ):
                # TODO: 视觉模型解释图像
                text_to_gpt.append(f"[{mark} 图片已生成，内容为 base64，未展示]")

                #  添加image到notebook
                if "png" in mark:
                    self.notebook_serializer.add_image_to_notebook(out_str, "image/png")
                    content_to_display.append(
                        ResultModel(type="result", format="png", msg=out_str)
                    )
                else:
                    self.notebook_serializer.add_image_to_notebook(
                        out_str, "image/jpeg"
                    )
                    content_to_display.append(
                        ResultModel(type="result", format="jpeg", msg=out_str)
                    )

            elif mark == "error":
                error_occurred = True
                error_message = self.delete_color_control_char(out_str)
                error_message = self._truncate_text(error_message)
                logger.error(f"执行错误: {error_message}")
                text_to_gpt.append(error_message)
                #  添加error到notebook
                self.notebook_serializer.add_code_cell_error_to_notebook(out_str)
                content_to_display.append(StdErrModel(msg=out_str))

        logger.info(f"text_to_gpt: {text_to_gpt}")
        combined_text = "\n".join(text_to_gpt)

        await self._push_to_websocket(content_to_display)

        return (
            combined_text,
            error_occurred,
            error_message,
        )

    def execute_code_(self, code) -> list[tuple[str, str]]:
        msg_id = self.kc.execute(code)
        logger.info(f"执行代码: {code}")
        # Get the output of the code
        msg_list = []
        while True:
            try:
                iopub_msg = self.kc.get_iopub_msg(timeout=1)
                msg_list.append(iopub_msg)
                if (
                    iopub_msg["msg_type"] == "status"
                    and iopub_msg["content"].get("execution_state") == "idle"
                ):
                    break
            except:
                if self.interrupt_signal:
                    self.km.interrupt_kernel()
                    self.interrupt_signal = False
                continue

        all_output: list[tuple[str, str]] = []
        for iopub_msg in msg_list:
            if iopub_msg["msg_type"] == "stream":
                if iopub_msg["content"].get("name") == "stdout":
                    output = iopub_msg["content"]["text"]
                    all_output.append(("stdout", output))
            elif iopub_msg["msg_type"] == "execute_result":
                if "data" in iopub_msg["content"]:
                    if "text/plain" in iopub_msg["content"]["data"]:
                        output = iopub_msg["content"]["data"]["text/plain"]
                        all_output.append(("execute_result_text", output))
                    if "text/html" in iopub_msg["content"]["data"]:
                        output = iopub_msg["content"]["data"]["text/html"]
                        all_output.append(("execute_result_html", output))
                    if "image/png" in iopub_msg["content"]["data"]:
                        output = iopub_msg["content"]["data"]["image/png"]
                        all_output.append(("execute_result_png", output))
                    if "image/jpeg" in iopub_msg["content"]["data"]:
                        output = iopub_msg["content"]["data"]["image/jpeg"]
                        all_output.append(("execute_result_jpeg", output))
            elif iopub_msg["msg_type"] == "display_data":
                if "data" in iopub_msg["content"]:
                    if "text/plain" in iopub_msg["content"]["data"]:
                        output = iopub_msg["content"]["data"]["text/plain"]
                        all_output.append(("display_text", output))
                    if "text/html" in iopub_msg["content"]["data"]:
                        output = iopub_msg["content"]["data"]["text/html"]
                        all_output.append(("display_html", output))
                    if "image/png" in iopub_msg["content"]["data"]:
                        output = iopub_msg["content"]["data"]["image/png"]
                        all_output.append(("display_png", output))
                    if "image/jpeg" in iopub_msg["content"]["data"]:
                        output = iopub_msg["content"]["data"]["image/jpeg"]
                        all_output.append(("display_jpeg", output))
            elif iopub_msg["msg_type"] == "error":
                # TODO: 正确返回格式
                if "traceback" in iopub_msg["content"]:
                    output = "\n".join(iopub_msg["content"]["traceback"])
                    cleaned_output = self.delete_color_control_char(output)
                    all_output.append(("error", cleaned_output))
        return all_output

    async def get_created_images(self, section: str) -> list[str]:
        """获取新创建的图片列表"""
        current_images = set()
        files = os.listdir(self.work_dir)
        for file in files:
            if file.endswith((".png", ".jpg", ".jpeg")):
                current_images.add(file)

        # 计算新增的图片
        new_images = current_images - self.last_created_images

        # 更新last_created_images为当前的图片集合
        self.last_created_images = current_images

        logger.info(f"新创建的图片列表: {new_images}")
        return list(new_images)  # 最后转换为list返回

    async def cleanup(self):
        # 关闭内核
        self.kc.shutdown()
        logger.info("关闭内核")
        self.km.shutdown_kernel()

    def send_interrupt_signal(self):
        self.interrupt_signal = True

    def restart_jupyter_kernel(self):
        """Restart the Jupyter kernel and recreate the work directory."""
        self.kc.shutdown()
        self.km, self.kc = jupyter_client.manager.start_new_kernel(
            kernel_name="python3"
        )
        self.interrupt_signal = False
        self._create_work_dir()

    def _create_work_dir(self):
        """Ensure the working directory exists after a restart."""
        os.makedirs(self.work_dir, exist_ok=True)
