"""
通用数据处理安全工具
防止因数据集列名差异导致的KeyError等问题
"""

import pandas as pd
from typing import List, Optional, Any, Dict
from app.utils.log_util import logger


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
        """
        安全获取列名，支持精确匹配和模糊匹配
        
        Args:
            possible_names: 可能的列名列表
            description: 列的描述（用于日志）
            fuzzy_match: 是否启用模糊匹配
            
        Returns:
            匹配到的列名或None
        """
        # 精确匹配
        for name in possible_names:
            if name in self.df.columns:
                logger.info(f"找到{description}的精确匹配: {name}")
                return name
        
        if fuzzy_match:
            # 模糊匹配
            for keyword in possible_names:
                matches = [col for col in self.df.columns if keyword in col]
                if matches:
                    logger.info(f"找到{description}的模糊匹配: {matches[0]} (关键词: {keyword})")
                    return matches[0]
        
        logger.warning(f"未找到{description}列，尝试的名称: {possible_names}")
        logger.info(f"可用列名: {self.df.columns.tolist()}")
        return None
    
    def safe_get_numeric_columns(self) -> List[str]:
        """获取所有数值型列"""
        return self.column_info['numeric_cols']
    
    def safe_get_categorical_columns(self) -> List[str]:
        """获取所有分类型列"""
        return self.column_info['categorical_cols']
    
    def safe_select_columns(self, column_names: List[str]) -> pd.DataFrame:
        """
        安全选择列，自动过滤不存在的列名
        
        Args:
            column_names: 要选择的列名列表
            
        Returns:
            包含存在列的DataFrame
        """
        existing_cols = [col for col in column_names if col in self.df.columns]
        missing_cols = [col for col in column_names if col not in self.df.columns]
        
        if missing_cols:
            logger.warning(f"以下列不存在，已自动跳过: {missing_cols}")
        
        if existing_cols:
            logger.info(f"成功选择列: {existing_cols}")
            return self.df[existing_cols]
        else:
            logger.error("没有找到任何指定的列")
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
        
        print("\n列名列表:")
        for i, col in enumerate(self.df.columns, 1):
            print(f"  {i:2d}. {col} ({self.df[col].dtype})")
        
        print(f"\n缺失值统计:")
        missing_info = self.df.isnull().sum()
        missing_cols = missing_info[missing_info > 0]
        if len(missing_cols) > 0:
            print(missing_cols)
        else:
            print("无缺失值")
            
        print(f"\n前5行数据:")
        print(self.df.head())
    
    def auto_detect_target_column(self) -> Optional[str]:
        """自动检测可能的目标变量列"""
        # 常见的目标变量列名模式
        target_patterns = [
            'label', 'target', '标签', '目标', '类别', '分类',
            'class', 'category', 'type', '类型', '结果', 'result',
            '行为特征', '特征', '状态', 'status'
        ]
        
        # 寻找可能的目标列
        for pattern in target_patterns:
            matched_col = self.safe_get_column([pattern], "目标变量", fuzzy_match=True)
            if matched_col:
                return matched_col
        
        # 如果找不到，返回最后一列（常见约定）
        if len(self.df.columns) > 0:
            last_col = self.df.columns[-1]
            logger.info(f"未找到明确的目标列，使用最后一列作为目标: {last_col}")
            return last_col
        
        return None


def create_safe_data_loader_code() -> str:
    """生成安全的数据加载代码模板"""
    return '''
# 导入安全数据处理工具
import pandas as pd
import numpy as np
from typing import List, Optional

# 安全数据加载和处理模板
def safe_load_and_process_data(file_path: str):
    """通用安全数据加载函数"""
    try:
        # 根据文件扩展名选择加载方式
        if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
            df = pd.read_excel(file_path)
        elif file_path.endswith('.csv'):
            df = pd.read_csv(file_path, encoding='utf-8')
        else:
            # 尝试多种编码
            for encoding in ['utf-8', 'gbk', 'gb2312']:
                try:
                    df = pd.read_csv(file_path, encoding=encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                raise ValueError("无法解码文件")
        
        print("数据加载成功！")
        return df
        
    except Exception as e:
        print(f"数据加载失败: {e}")
        return None

# 使用示例：
# df = safe_load_and_process_data("your_data_file.csv")
# if df is not None:
#     processor = SafeDataProcessor(df)
#     processor.print_data_summary()
'''


# 为代码执行环境注入安全工具
def inject_safe_tools():
    """返回要注入到代码执行环境的安全工具代码"""
    with open(__file__, 'r', encoding='utf-8') as f:
        return f.read()