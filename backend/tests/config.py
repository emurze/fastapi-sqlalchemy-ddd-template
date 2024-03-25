from typing import ClassVar

from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings

from config import TopLevelConfig
from seedwork.infra.logging import LogLevel


class TestDatabaseConfig(BaseSettings):
    test_db_name: str
    test_db_user: str
    test_db_pass: SecretStr
    test_db_host: str
    test_db_port: int
    driver: ClassVar[str] = "postgresql+asyncpg"

    @classmethod
    def get_dsn(cls) -> str:
        self = cls()
        return "{}://{}:{}@{}:{}/{}".format(
            self.driver,
            self.test_db_user,
            self.test_db_pass.get_secret_value(),
            self.test_db_host,
            self.test_db_port,
            self.test_db_name,
        )


class TestCacheConfig(BaseSettings):
    test_cache_port: int
    test_cache_host: str
    test_cache_db: int
    driver: ClassVar[str] = "redis"

    @classmethod
    def get_dsn(cls) -> str:
        self = cls()
        return "{}://{}:{}/{}".format(
            self.driver,
            self.test_cache_host,
            self.test_cache_port,
            self.test_cache_db,
        )


class TestTopLevelConfig(BaseSettings):
    project_title: str = Field(validation_alias="test_project_title")
    db_dsn: str = Field(default_factory=TestDatabaseConfig.get_dsn)
    cache_dsn: str = Field(default_factory=TestCacheConfig.get_dsn)


def get_top_config() -> TopLevelConfig:
    test_config = TestTopLevelConfig()
    return TopLevelConfig(
        log_level=LogLevel.debug,
        project_title=test_config.project_title,
        db_dsn=test_config.db_dsn,
        cache_dsn=test_config.cache_dsn,
    )
