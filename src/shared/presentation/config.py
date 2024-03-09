from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings

from shared.infra.redis.cache.config import cache_config
from shared.infra.sqlalchemy_orm.config import db_config


class TopLevelConfig(BaseSettings):
    secret_key: SecretStr
    project_title: str
    log_level: str
    db_dsn: str = Field(default_factory=db_config.get_dsn)
    cache_dsn: str = Field(default_factory=cache_config.get_dsn)
