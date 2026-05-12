"""Checkpoint 管理模块，基于 Redis 持久化的 HIL 审批流程。"""

from typing import Any

from app.config.setting import settings
from app.schemas.response import ApprovalMessage
from app.services.redis_manager import redis_manager
from app.services.state_store import state_store
from app.utils.log_util import logger


class CheckpointManager:
    """基于 Redis 的检查点管理器，实现 HIL 审批等待和决策提交。"""

    def _decision_key(self, task_id: str, checkpoint_id: str) -> str:
        """构建决策存储的键名。"""
        return f"{task_id}:{checkpoint_id}"

    async def wait_for_decision(
        self,
        task_id: str,
        checkpoint_id: str,
        prompt: dict,
        timeout: int | None = None,
    ) -> dict[str, Any]:
        """发送审批请求并等待用户决策。

        Args:
            task_id: 任务 ID。
            checkpoint_id: 检查点 ID。
            prompt: 审批提示内容（包含当前 Agent 输出等上下文）。
            timeout: 超时时间（秒），默认使用配置值。

        Returns:
            用户决策字典，格式: {"action": "confirm"|"edit"|..., "content": ...}
            超时时返回 {"action": "confirm"}（自动继续）。
        """
        timeout = timeout or settings.HIL_TIMEOUT

        # 发送审批消息到前端
        approval_msg = ApprovalMessage(
            checkpoint_id=checkpoint_id,
            prompt=prompt,
            timeout=timeout,
        )
        await redis_manager.publish_message(task_id, approval_msg)
        logger.info(
            f"CheckpointManager: 发送审批请求 checkpoint={checkpoint_id}, timeout={timeout}s"
        )

        # 轮询 Redis 等待决策
        decision = await state_store.wait_for_update(
            namespace="checkpoint",
            key=self._decision_key(task_id, checkpoint_id),
            timeout=timeout,
        )

        if decision is None:
            # 超时，自动继续
            logger.warning(
                f"CheckpointManager: checkpoint={checkpoint_id} 超时，自动 confirm"
            )
            return {"action": "confirm"}

        logger.info(
            f"CheckpointManager: 收到决策 checkpoint={checkpoint_id}, action={decision.get('action')}"
        )
        return decision

    async def submit_decision(
        self,
        task_id: str,
        checkpoint_id: str,
        decision: dict[str, Any],
    ) -> None:
        """提交用户决策到 Redis，唤醒等待的 workflow。

        Args:
            task_id: 任务 ID。
            checkpoint_id: 检查点 ID。
            decision: 用户决策字典。
        """
        await state_store.set(
            namespace="checkpoint",
            key=self._decision_key(task_id, checkpoint_id),
            value=decision,
            ttl=3600,  # 1 小时过期
        )
        logger.info(
            f"CheckpointManager: 提交决策 checkpoint={checkpoint_id}, action={decision.get('action')}"
        )


# 全局单例
checkpoint_manager = CheckpointManager()
