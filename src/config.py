import os

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from enum import StrEnum


class Environ(StrEnum):
    PRD = "PRD"
    DEV = "DEV"


def get_env_file_name(env_key: str) -> str:
    env_key_normalized = env_key if env_key.upper() in Environ else Environ.DEV
    env_file_mapper: dict[Environ, str] = {
        Environ.PRD: ".env",
        Environ.DEV: ".env.dev",
    }
    return env_file_mapper.get(env_key_normalized, ".env.dev")


class DatabaseConfig(BaseSettings):
    url: str = Field(default="DATABASE_URL", alias="DATABASE_URL")
    sqlalchemy_url: str = Field(
        default="SQLALCHEMY_DATABASE_URL", alias="SQLALCHEMY_DATABASE_URL"
    )
    echo: bool = Field(default=True, alias="DATABASE_ECHO")
    model_config = SettingsConfigDict(
        env_file=get_env_file_name(os.getenv("CONF_ENV")),
        env_file_encoding="utf-8",
    )


class CORSConfig(BaseSettings):
    origins: str = Field(default="*", alias="CORS_ORIGINS")
    credentials: bool = Field(default=True, alias="CORS_CREDENTIALS")
    methods: str = Field(default="*", alias="CORS_METHODS")
    headers: str = Field(default="*", alias="CORS_HEADERS")


class WebConfig(BaseSettings):
    host: str = Field(default="0.0.0.0", alias="WEB_HOST")
    port: int = Field(default=8000, alias="WEB_PORT")


db = DatabaseConfig()
cors = CORSConfig()
web = WebConfig()
