from pydantic import AnyUrl, BeforeValidator, computed_field, field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
import os
from typing import Annotated, Optional


def parse_cors(value: str) -> list[str]:
    """
    Parses the CORS settings from a string to a list of URLs.
    """
    if value == "*":
        return ["*"]
    if "," in value:
        return [url.strip() for url in value.split(",")]
    return [value]


class Settings(BaseSettings):
    ENV: str

    COORDINATOR_API_KEY: Optional[str] = None
    COORDINATOR_MODEL: Optional[str] = None
    COORDINATOR_BASE_URL: Optional[str] = None

    MODELER_API_KEY: Optional[str] = None
    MODELER_MODEL: Optional[str] = None
    MODELER_BASE_URL: Optional[str] = None

    CODER_API_KEY: Optional[str] = None
    CODER_MODEL: Optional[str] = None
    CODER_BASE_URL: Optional[str] = None

    WRITER_API_KEY: Optional[str] = None
    WRITER_MODEL: Optional[str] = None
    WRITER_BASE_URL: Optional[str] = None

    MAX_CHAT_TURNS: int = 60
    MAX_RETRIES: int = 5
    E2B_API_KEY: Optional[str] = None
    LOG_LEVEL: str = "DEBUG"
    DEBUG: bool = True
    REDIS_URL: str = "redis://redis:6379/0"
    REDIS_MAX_CONNECTIONS: int = 10
    CORS_ALLOW_ORIGINS: Annotated[list[str] | str, BeforeValidator(parse_cors)] = "*"
    SERVER_HOST: str = "http://localhost:8000"
    OPENALEX_EMAIL: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env.dev",
        env_file_encoding="utf-8",
        extra="allow",
    )

    @classmethod
    def from_env(cls, env: str = None):
        env = env or os.getenv("ENV", "dev")
        env_file = f".env.{env.lower()}"
        return cls(_env_file=env_file, _env_file_encoding="utf-8")


settings = Settings()
