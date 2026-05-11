"""日志初始化模块，配置 loguru 日志格式和输出。"""

import os
import sys
import time
from loguru import logger as _logger  # type: ignore[import-unresolved]


class LoggerInitializer:
    """日志初始化器，配置控制台和文件日志输出。"""
    def __init__(self):
        self.log_path = os.path.join(os.getcwd(), "logs")
        self.__ensure_log_directory_exists()
        self.log_path_error = os.path.join(
            self.log_path, f"{time.strftime('%Y-%m-%d')}_error.log"
        )

    def __ensure_log_directory_exists(self):
        """
        确保日志目录存在，如果不存在则创建
        """
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)

    @staticmethod
    def __filter(log: dict):
        """
        自定义日志过滤器，添加trace_id
        """
        return log

    def init_log(self):
        """
        初始化日志配置
        """
        # 自定义日志格式
        format_str = (
            "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        )
        _logger.remove()
        # 移除后重新添加sys.stderr, 目的: 控制台输出与文件日志内容和结构一致
        _logger.add(sys.stderr, filter=self.__filter, format=format_str, enqueue=False)
        _logger.add(
            self.log_path_error,
            filter=self.__filter,
            format=format_str,
            rotation="50MB",
            encoding="utf-8",
            enqueue=False,
            compression="zip",
        )

        return _logger


# 初始化日志处理器
log_initializer = LoggerInitializer()
logger = log_initializer.init_log()
