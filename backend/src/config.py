from typing import Optional

from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings

from seedwork.infra.logging import LogLevel


class PubsubConfig(BaseSettings):
    pubsub_driver: str = "redis"
    pubsub_host: str
    pubsub_port: int
    pubsub_db: int

    @classmethod
    def get_dsn(cls) -> str:
        self = cls()
        return "{}://{}:{}/{}".format(
            self.pubsub_driver,
            self.pubsub_host,
            self.pubsub_port,
            self.pubsub_db,
        )


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
    secret_key: SecretStr
    project_title: str
    host: str
    port: int
    debug: Optional[bool] = None
    db_echo: bool = False
    db_dsn: str = Field(default_factory=DatabaseConfig.get_dsn)
    cache_dsn: str = Field(default_factory=CacheConfig.get_dsn)
    pubsub_dsn: str = Field(default_factory=PubsubConfig.get_dsn)
    log_level_in: Optional[str] = Field(None, validation_alias="log_level")

    @property
    def log_level(self) -> str:
        if self.log_level_in:
            return self.log_level_in.lower()

        if self.debug:
            return LogLevel.debug.lower()

        return LogLevel.warning.lower()
