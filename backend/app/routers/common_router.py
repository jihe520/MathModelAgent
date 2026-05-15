"""通用路由模块，提供配置查询、消息获取和健康检查等接口。"""

import json
from pathlib import Path

from aiofile import async_open
from fastapi import APIRouter, HTTPException
from app.config.setting import settings
from app.utils.common_utils import ensure_safe_task_id, get_config_template
from app.schemas.enums import CompTemplate
from app.services.redis_manager import redis_manager
from app.utils.log_util import logger

router = APIRouter()


def _require_safe_task_id(task_id: str) -> str:
    """验证并返回安全的任务 ID。

    Args:
        task_id: 待验证的任务 ID。

    Returns:
        验证通过的任务 ID。

    Raises:
        HTTPException: 任务 ID 非法时返回 400。
    """
    try:
        return ensure_safe_task_id(task_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="非法任务ID") from exc


async def _load_task_messages_from_file(task_id: str) -> list[dict]:
    """从文件加载指定任务的历史消息。

    Args:
        task_id: 任务 ID。

    Returns:
        消息列表，文件不存在时返回空列表。
    """
    safe_task_id = _require_safe_task_id(task_id)
    message_file = Path("logs/messages") / f"{safe_task_id}.json"
    if not message_file.exists():
        return []

    try:
        async with async_open(message_file, "r", encoding="utf-8") as f:
            content = await f.read()
            data = json.loads(content)
        return data if isinstance(data, list) else []
    except Exception as e:
        logger.error(f"读取任务消息文件失败: {str(e)}")
        return []


@router.get("/")
async def root():
    return {"message": "Hello World"}


@router.get("/config")
async def config():
    return {
        "environment": settings.ENV,
        "deepseek_model": settings.DEEPSEEK_MODEL,
        "deepseek_base_url": settings.DEEPSEEK_BASE_URL,
        "max_chat_turns": settings.MAX_CHAT_TURNS,
        "max_retries": settings.MAX_RETRIES,
        "CORS_ALLOW_ORIGINS": settings.CORS_ALLOW_ORIGINS,
    }


@router.get("/writer_seque")
async def get_writer_seque():
    # 返回论文顺序
    config_template: dict = get_config_template(CompTemplate.CHINA)
    return list(config_template.keys())


@router.get("/messages")
async def get_task_messages(task_id: str):
    return await _load_task_messages_from_file(task_id)


@router.get("/track")
async def track(task_id: str):
    # 获取任务的token使用情况

    pass


@router.get("/status")
async def get_service_status():
    """获取后端和 Redis 的运行状态。"""
    status = {
        "backend": {"status": "running", "message": "Backend service is running"},
        "redis": {"status": "unknown", "message": "Redis connection status unknown"}
    }

    # 检查Redis连接状态
    try:
        redis_client = await redis_manager.get_client()
        await redis_client.ping()  # type: ignore[reportGeneralTypeIssues]
        status["redis"] = {"status": "running", "message": "Redis connection is healthy"}
    except Exception as e:
        logger.error(f"Redis connection failed: {str(e)}")
        status["redis"] = {"status": "error", "message": f"Redis connection failed: {str(e)}"}

    return status
