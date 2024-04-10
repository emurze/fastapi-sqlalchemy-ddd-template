import logging

from enum import StrEnum
from typing import Optional

from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings

LOG_FORMAT_DEBUG = (
    "%(levelname)s:     %(message)s  %(pathname)s:%(funcName)s:%(lineno)d"
)


class LogLevel(StrEnum):
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    debug = "DEBUG"


class CacheConfig(BaseSettings):
    cache_driver: str = "redis"
    cache_host: str
    cache_port: int
    cache_db: int

    @classmethod
    def get_dsn(cls) -> str:
        self = cls()
        return "{}://{}:{}/{}".format(
            self.cache_driver,
            self.cache_host,
            self.cache_port,
            self.cache_db,
        )


class DatabaseConfig(BaseSettings):
    db_driver: str = "postgresql+asyncpg"
    db_name: str
    db_user: str
    db_pass: SecretStr
    db_host: str
    db_port: int

    @classmethod
    def get_dsn(cls) -> str:
        self = cls()
        return "{}://{}:{}@{}:{}/{}".format(
            self.db_driver,
            self.db_user,
            self.db_pass.get_secret_value(),
            self.db_host,
            self.db_port,
            self.db_name,
        )


class TopLevelConfig(BaseSettings):
    debug: bool = False
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_prefix: str = ""
    openapi_url: str = "/openapi.json"
    secret_key: SecretStr
    title: str = "Online shop"
    version: str = "0.0.0"
    host: str
    port: int
    encoding: str = "utf8"
    allowed_origins: list[str] = ["http://frontend:3000"]

    pool_size: int = 10
    pool_max_overflow: int = 0
    db_echo: bool = False
    db_dsn: str = Field(default_factory=DatabaseConfig.get_dsn)

    cache_dsn: str = Field(default_factory=CacheConfig.get_dsn)

    log_level_in: Optional[str] = Field(None, validation_alias="log_level")

    @property
    def log_level(self) -> str:
        if self.log_level_in:
            return self.log_level_in.lower()

        if self.debug:
            return LogLevel.debug.lower()

        return LogLevel.warning.lower()

    def configure_logging(self) -> None:
        log_level = self.log_level.upper()
        log_levels = list(LogLevel)

        if log_level not in log_levels:
            # We use LogLevel.error as the default log level
            logging.basicConfig(level=LogLevel.error)
            return

        if log_level == LogLevel.debug:
            logging.basicConfig(level=log_level, format=LOG_FORMAT_DEBUG)
            return

        logging.basicConfig(level=log_level)
