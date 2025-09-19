from typing import Dict
import httpx
import asyncio
from app.tools.base_interpreter import BaseCodeInterpreter
from app.config.setting import settings
from app.utils.log_util import logger


class SandboxManager:
    """
    SandboxManager is a class that manages the active sandboxes.
    """

    def __init__(self):
        self.active_sandbox: Dict[str, BaseCodeInterpreter] = {}

    def get_interpreter(
        self, session_id: str, e2b_api_key: str | None = None
    ) -> BaseCodeInterpreter:
        if session_id not in self.active_sandbox:
            self.active_sandbox[session_id] = BaseCodeInterpreter(
                timeout=60 * 60,
            )
        return self.active_sandbox[session_id]

    async def check_sandbox_status(self) -> dict:
        """
        检查sandbox服务状态
        """
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(f"{settings.SANDBOX_SERVICE_URL}/status")
                if response.status_code == 200:
                    data = response.json()
                    return {
                        "status": "running",
                        "message": f"Sandbox service is running: {data.get('message', '')}",
                    }
                else:
                    return {
                        "status": "error",
                        "message": f"Sandbox service returned status code {response.status_code}",
                    }
        except httpx.ConnectError:
            logger.error(
                f"Cannot connect to sandbox service at {settings.SANDBOX_SERVICE_URL}"
            )
            return {
                "status": "error",
                "message": f"Cannot connect to sandbox service at {settings.SANDBOX_SERVICE_URL}",
            }
        except httpx.TimeoutException:
            logger.error("Sandbox service request timeout")
            return {"status": "error", "message": "Sandbox service request timeout"}
        except Exception as e:
            logger.error(f"Sandbox service check failed: {str(e)}")
            return {
                "status": "error",
                "message": f"Sandbox service check failed: {str(e)}",
            }


## clean sandbox

sandbox_manager = SandboxManager()
