import json
from pathlib import Path

from fastapi import APIRouter, HTTPException
from app.config.setting import settings
from app.utils.common_utils import ensure_safe_task_id, get_config_template
from app.schemas.enums import CompTemplate
from app.services.redis_manager import redis_manager
from app.utils.log_util import logger

router = APIRouter()


def _require_safe_task_id(task_id: str) -> str:
    try:
        return ensure_safe_task_id(task_id)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="非法任务ID") from exc


def _load_task_messages_from_file(task_id: str) -> list[dict]:
    safe_task_id = _require_safe_task_id(task_id)
    message_file = Path("logs/messages") / f"{safe_task_id}.json"
    if not message_file.exists():
        return []

    try:
        with open(message_file, "r", encoding="utf-8") as f:
            data = json.load(f)
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
    return _load_task_messages_from_file(task_id)


@router.get("/track")
async def track(task_id: str):
    # 获取任务的token使用情况

    pass


@router.get("/status")
async def get_service_status():
    """获取各个服务的状态"""
    status = {
        "backend": {"status": "running", "message": "Backend service is running"},
        "redis": {"status": "unknown", "message": "Redis connection status unknown"}
    }

    # 检查Redis连接状态
    try:
        redis_client = await redis_manager.get_client()
        await redis_client.ping()
        status["redis"] = {"status": "running", "message": "Redis connection is healthy"}
    except Exception as e:
        logger.error(f"Redis connection failed: {str(e)}")
        status["redis"] = {"status": "error", "message": f"Redis connection failed: {str(e)}"}

    return status
