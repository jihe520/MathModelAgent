import redis.asyncio as aioredis
from typing import Optional
import json
from pathlib import Path
from app.config.setting import settings
from app.schemas.response import Message
from app.utils.log_util import logger


class RedisManager:
    def __init__(self):
        self.redis_url = settings.REDIS_URL
        self._client: Optional[aioredis.Redis] = None
        # 创建消息存储目录
        self.messages_dir = Path("logs/messages")
        self.messages_dir.mkdir(parents=True, exist_ok=True)

    async def get_client(self) -> aioredis.Redis:
        if self._client is None:
            self._client = aioredis.Redis.from_url(
                self.redis_url,
                decode_responses=True,
                max_connections=settings.REDIS_MAX_CONNECTIONS,
            )
        try:
            await self._client.ping()
            logger.info(f"Redis 连接建立成功: {self.redis_url}")
            return self._client
        except Exception as e:
            logger.error(f"无法连接到Redis: {str(e)}")
            raise

    async def set(self, key: str, value: str):
        """设置Redis键值对"""
        client = await self.get_client()
        await client.set(key, value)
        await client.expire(key, 36000)

    async def _save_message_to_file(self, task_id: str, message: Message):
        """将消息保存到文件中，同一任务的消息保存在同一个文件中"""
        try:
            # 确保目录存在
            self.messages_dir.mkdir(exist_ok=True)

            # 使用任务ID作为文件名
            file_path = self.messages_dir / f"{task_id}.json"

            # 读取现有消息（如果文件存在）
            messages = []
            if file_path.exists():
                with open(file_path, "r", encoding="utf-8") as f:
                    messages = json.load(f)

            # 添加新消息
            message_data = message.model_dump()
            messages.append(message_data)

            # 保存所有消息到文件
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(messages, f, ensure_ascii=False, indent=2)

            logger.debug(f"消息已追加到文件: {file_path}")
        except Exception as e:
            logger.error(f"保存消息到文件失败: {str(e)}")
            # 不抛出异常，确保主流程不受影响

    async def publish_message(self, task_id: str, message: Message):
        """发布消息到特定任务的频道并保存到文件"""
        client = await self.get_client()
        channel = f"task:{task_id}:messages"
        try:
            message_json = message.model_dump_json()
            await client.publish(channel, message_json)
            logger.debug(
                f"消息已发布到频道 {channel}:mes_type:{message.msg_type}:msg_content:{message.content}"
            )
            # 保存消息到文件
            await self._save_message_to_file(task_id, message)
        except Exception as e:
            logger.error(f"发布消息失败: {str(e)}")
            raise

    async def subscribe_to_task(self, task_id: str):
        """订阅特定任务的消息"""
        client = await self.get_client()
        pubsub = client.pubsub()
        await pubsub.subscribe(f"task:{task_id}:messages")
        return pubsub

    async def close(self):
        """关闭Redis连接"""
        if self._client:
            await self._client.close()
            self._client = None


redis_manager = RedisManager()
