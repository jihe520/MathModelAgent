"""应用配置模块，基于 pydantic-settings 管理环境变量和全局配置。"""

from pydantic import BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from typing import Annotated, Optional


def parse_cors(value: str) -> list[str]:
    """将 CORS 配置字符串解析为 URL 列表。

    Args:
        value: 逗号分隔的 URL 字符串，或 "*" 表示允许所有来源。

    Returns:
        解析后的 URL 列表。
    """
    if value == "*":
        return ["*"]
    if "," in value:
        return [url.strip() for url in value.split(",")]
    return [value]


class Settings(BaseSettings):
    """全局应用配置，从环境变量和 .env 文件加载。"""
    ENV: str = "dev"

    COORDINATOR_API_KEY: Optional[str] = None
    COORDINATOR_MODEL: Optional[str] = None
    COORDINATOR_BASE_URL: Optional[str] = None
    COORDINATOR_MAX_TOKENS: Optional[int] = None

    MODELER_API_KEY: Optional[str] = None
    MODELER_MODEL: Optional[str] = None
    MODELER_BASE_URL: Optional[str] = None
    MODELER_MAX_TOKENS: Optional[int] = None

    CODER_API_KEY: Optional[str] = None
    CODER_MODEL: Optional[str] = None
    CODER_BASE_URL: Optional[str] = None
    CODER_MAX_TOKENS: Optional[int] = None

    WRITER_API_KEY: Optional[str] = None
    WRITER_MODEL: Optional[str] = None
    WRITER_BASE_URL: Optional[str] = None
    WRITER_MAX_TOKENS: Optional[int] = None

    MAX_CHAT_TURNS: Optional[int] = None
    MAX_RETRIES: Optional[int] = None
    E2B_API_KEY: Optional[str] = None
    LOG_LEVEL: str = "DEBUG"
    DEBUG: bool = True
    REDIS_URL: str = "redis://redis:6379/0"
    REDIS_MAX_CONNECTIONS: int = 10
    CORS_ALLOW_ORIGINS: Annotated[list[str] | str, BeforeValidator(parse_cors)] = "*"
    SERVER_HOST: str = "http://localhost:8000"
    DEEPSEEK_MODEL: Optional[str] = None
    DEEPSEEK_BASE_URL: Optional[str] = None
    OPENALEX_EMAIL: Optional[str] = None
    OPENALEX_API_KEY: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env.dev",
        env_file_encoding="utf-8",
        extra="allow",
    )

    @classmethod
    def from_env(cls, env: str | None = None):
        """根据环境名称加载对应配置。

        Args:
            env: 环境名称（如 dev、prod），默认从 ENV 环境变量获取。
        """
        env = env or os.getenv("ENV", "dev")
        env_file = f".env.{env.lower()}"
        return cls(_env_file=env_file, _env_file_encoding="utf-8")  # type: ignore[call-arg]


settings = Settings()
