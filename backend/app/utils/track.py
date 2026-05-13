"""LLM 调用指标收集模块。"""

from app.utils.log_util import logger


def log_agent_call(agent_name: str, success: bool = True) -> None:
    """记录 LLM 调用日志。

    Args:
        agent_name: Agent 名称。
        success: 调用是否成功。
    """
    status = "成功" if success else "失败"
    logger.info(f"LLM 调用 {status}: {agent_name}")
