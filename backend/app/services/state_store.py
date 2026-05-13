"""基于 Redis 的持久化状态存储模块。"""

import asyncio
import json
from typing import Any

from app.services.redis_manager import redis_manager
from app.utils.log_util import logger


class StateStore:
    """Redis 持久化状态存储，支持 HIL checkpoint 等待和搜索缓存。"""

    def _make_key(self, namespace: str, key: str) -> str:
        """构建 Redis 键名。"""
        return f"state:{namespace}:{key}"

    async def set(
        self, namespace: str, key: str, value: Any, ttl: int | None = None
    ) -> None:
        """存储键值对。

        Args:
            namespace: 命名空间（如 "search", "checkpoint"）。
            key: 键名。
            value: 值（会被 JSON 序列化）。
            ttl: 过期时间（秒），None 表示不过期。
        """
        client = await redis_manager.get_client()
        redis_key = self._make_key(namespace, key)
        serialized = json.dumps(value, ensure_ascii=False)
        await client.set(redis_key, serialized)
        if ttl is not None:
            await client.expire(redis_key, ttl)
        logger.debug(f"StateStore: set {redis_key} (ttl={ttl})")

    async def get(self, namespace: str, key: str) -> Any | None:
        """读取键值。

        Args:
            namespace: 命名空间。
            key: 键名。

        Returns:
            存储的值，不存在时返回 None。
        """
        client = await redis_manager.get_client()
        redis_key = self._make_key(namespace, key)
        raw = await client.get(redis_key)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            return raw

    async def delete(self, namespace: str, key: str) -> None:
        """删除键值对。

        Args:
            namespace: 命名空间。
            key: 键名。
        """
        client = await redis_manager.get_client()
        redis_key = self._make_key(namespace, key)
        await client.delete(redis_key)
        logger.debug(f"StateStore: delete {redis_key}")

    async def wait_for_update(
        self, namespace: str, key: str, timeout: float = 300
    ) -> Any | None:
        """等待状态更新（轮询 Redis，用于 HIL checkpoint）。

        Args:
            namespace: 命名空间。
            key: 键名。
            timeout: 超时时间（秒）。

        Returns:
            更新后的值，超时返回 None。
        """
        redis_key = self._make_key(namespace, key)
        client = await redis_manager.get_client()
        poll_interval = 1.0
        elapsed = 0.0

        # 先检查是否已有值（避免已写入时还等待）
        raw = await client.get(redis_key)
        if raw is not None:
            try:
                return json.loads(raw)
            except (json.JSONDecodeError, TypeError):
                return raw

        while elapsed < timeout:
            await asyncio.sleep(poll_interval)
            elapsed += poll_interval
            raw = await client.get(redis_key)
            if raw is not None:
                try:
                    return json.loads(raw)
                except (json.JSONDecodeError, TypeError):
                    return raw

        logger.warning(f"StateStore: wait_for_update {redis_key} 超时 ({timeout}s)")
        return None


# 全局单例
state_store = StateStore()
