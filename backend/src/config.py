from typing import Optional

from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings

from shared.infra.logging import LogLevel
from shared.infra.redis.cache.config import cache_config
from shared.infra.sqlalchemy_orm.config import db_config


class TopLevelConfig(BaseSettings):
    secret_key: SecretStr
    project_title: str
    host: str
    port: int
    debug: Optional[bool] = None
    db_dsn: str = Field(default_factory=db_config.get_dsn)
    cache_dsn: str = Field(default_factory=cache_config.get_dsn)
    log_level_: Optional[str] = Field(None, validation_alias="log_level")

    @property
    def log_level(self) -> str:
        if self.log_level_:
            return self.log_level_in.lower()

        if self.debug:
            return LogLevel.debug.lower()

        return LogLevel.warning.lower()
