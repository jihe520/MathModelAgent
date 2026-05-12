"""WebSocket 路由模块，提供双向实时任务消息推送。"""

import asyncio
import json

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState

from app.schemas.response import SystemMessage
from app.services.redis_manager import redis_manager
from app.services.state_store import state_store
from app.services.ws_manager import ws_manager
from app.utils.common_utils import ensure_safe_task_id
from app.utils.log_util import logger

router = APIRouter()


def _is_websocket_closed(websocket: WebSocket) -> bool:
    return (
        websocket.client_state == WebSocketState.DISCONNECTED
        or websocket.application_state == WebSocketState.DISCONNECTED
    )


def _is_closed_send_error(error: Exception) -> bool:
    text = str(error)
    return (
        'Cannot call "send" once a close message has been sent' in text
        or "Unexpected ASGI message 'websocket.send'" in text
    )


async def _handle_client_message(task_id: str, data: dict) -> None:
    """处理客户端发来的消息。

    Args:
        task_id: 任务 ID。
        data: 客户端消息字典。
    """
    msg_type = data.get("type")

    if msg_type == "user_decision":
        # HIL 审批决策
        checkpoint_id = data.get("checkpoint_id", "")
        decision = data.get("decision", {})
        if checkpoint_id and decision:
            await state_store.set(
                namespace="checkpoint",
                key=f"{task_id}:{checkpoint_id}",
                value=decision,
                ttl=3600,
            )
            logger.info(
                f"收到用户决策: task={task_id}, checkpoint={checkpoint_id}, action={decision.get('action')}"
            )
        else:
            logger.warning(f"收到格式错误的 user_decision: {data}")
    else:
        logger.warning(f"收到未知类型的客户端消息: type={msg_type}")


async def _listen_client(websocket: WebSocket, task_id: str) -> None:
    """监听客户端发来的消息。

    Args:
        websocket: WebSocket 连接。
        task_id: 任务 ID。
    """
    try:
        while not _is_websocket_closed(websocket):
            try:
                raw = await websocket.receive_text()
                data = json.loads(raw)
                await _handle_client_message(task_id, data)
            except WebSocketDisconnect:
                logger.info(f"客户端断开连接: task={task_id}")
                break
            except json.JSONDecodeError as e:
                logger.warning(f"客户端消息 JSON 解析失败: {e}")
            except Exception as e:
                if _is_websocket_closed(websocket):
                    break
                logger.error(f"处理客户端消息时出错: {e}")
    except Exception as e:
        if not _is_websocket_closed(websocket):
            logger.error(f"客户端监听异常: {e}")


async def _forward_server_messages(websocket: WebSocket, pubsub, task_id: str) -> None:
    """转发 Redis PubSub 消息到客户端。

    Args:
        websocket: WebSocket 连接。
        pubsub: Redis PubSub 实例。
        task_id: 任务 ID。
    """
    try:
        while True:
            if _is_websocket_closed(websocket):
                logger.info(f"WebSocket 已关闭，停止转发 task_id: {task_id}")
                break
            try:
                msg = await pubsub.get_message(ignore_subscribe_messages=True)
                if msg:
                    try:
                        msg_dict = json.loads(msg["data"])
                    except Exception as e:
                        logger.error(f"Error parsing websocket payload: {e}")
                        if _is_websocket_closed(websocket):
                            break
                        try:
                            await ws_manager.send_personal_message_json(
                                SystemMessage(
                                    content="实时消息解析失败，已忽略异常数据。",
                                    type="error",
                                ).model_dump(),
                                websocket,
                            )
                        except WebSocketDisconnect:
                            logger.info(
                                "WebSocket disconnected while sending parse error notice"
                            )
                            break
                        except RuntimeError as send_error:
                            if _is_closed_send_error(send_error):
                                logger.info("WebSocket 已关闭，跳过解析失败提示发送")
                                break
                            raise
                    else:
                        try:
                            await ws_manager.send_personal_message_json(
                                msg_dict, websocket
                            )
                        except WebSocketDisconnect:
                            logger.info("WebSocket disconnected while sending message")
                            break
                        except RuntimeError as send_error:
                            if _is_closed_send_error(send_error):
                                logger.info(
                                    f"WebSocket 已关闭，停止发送后续消息 task_id: {task_id}"
                                )
                                break
                            raise
                await asyncio.sleep(0.1)

            except WebSocketDisconnect:
                logger.info("WebSocket disconnected")
                break
            except Exception as e:
                if _is_closed_send_error(e) or _is_websocket_closed(websocket):
                    logger.info(
                        f"WebSocket 发送通道已关闭，结束循环 task_id: {task_id}"
                    )
                    break
                logger.error(f"Error in websocket loop: {e}")
                await asyncio.sleep(1)
                continue

    except Exception as e:
        logger.error(f"WebSocket error: {e}")


@router.websocket("/task/{task_id}")
async def websocket_endpoint(websocket: WebSocket, task_id: str):
    try:
        safe_task_id = ensure_safe_task_id(task_id)
    except ValueError:
        logger.warning(f"WebSocket task_id 非法: {task_id}")
        await websocket.close(code=1008, reason="Invalid task id")
        return

    logger.info(f"WebSocket 尝试连接 task_id: {safe_task_id}")

    redis_async_client = await redis_manager.get_client()
    if not await redis_async_client.exists(f"task_id:{safe_task_id}"):
        logger.warning(f"Task not found: {safe_task_id}")
        await websocket.close(code=1008, reason="Task not found")
        return
    logger.info(f"WebSocket connected for task: {safe_task_id}")

    # 建立 WebSocket 连接
    await ws_manager.connect(websocket)
    logger.debug(f"WebSocket connection status: {websocket.client}")

    # 订阅 Redis 频道
    pubsub = await redis_manager.subscribe_to_task(safe_task_id)
    logger.debug(f"Subscribed to Redis channel: task:{safe_task_id}:messages")

    try:
        # 双向并发：服务端消息转发 + 客户端消息监听
        forward_task = asyncio.create_task(
            _forward_server_messages(websocket, pubsub, safe_task_id)
        )
        listen_task = asyncio.create_task(_listen_client(websocket, safe_task_id))

        # 等待任一任务结束（通常是客户端断开）
        done, pending = await asyncio.wait(
            [forward_task, listen_task],
            return_when=asyncio.FIRST_COMPLETED,
        )
        # 取消未完成的任务
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass

    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        await pubsub.unsubscribe(f"task:{safe_task_id}:messages")
        ws_manager.disconnect(websocket)
        logger.info(f"WebSocket connection closed for task: {safe_task_id}")
