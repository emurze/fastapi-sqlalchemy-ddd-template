from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings

from config import TopLevelConfig
from seedwork.infra.logging import LogLevel


class TestPubsubConfig(BaseSettings):
    test_pubsub_driver: str = "redis"
    test_pubsub_host: str
    test_pubsub_port: int
    test_pubsub_db: int

    @classmethod
    def get_dsn(cls) -> str:
        self = cls()
        return "{}://{}:{}/{}".format(
            self.test_pubsub_driver,
            self.test_pubsub_host,
            self.test_pubsub_port,
            self.test_pubsub_db,
        )


class TestDatabaseConfig(BaseSettings):
    test_db_name: str
    test_db_user: str
    test_db_pass: SecretStr
    test_db_host: str
    test_db_port: int
    test_db_driver: str = "postgresql+asyncpg"

    @classmethod
    def get_dsn(cls) -> str:
        self = cls()
        return "{}://{}:{}@{}:{}/{}".format(
            self.test_db_driver,
            self.test_db_user,
            self.test_db_pass.get_secret_value(),
            self.test_db_host,
            self.test_db_port,
            self.test_db_name,
        )


class TestCacheConfig(BaseSettings):
    test_cache_driver: str = "redis"
    test_cache_port: int
    test_cache_host: str
    test_cache_db: int

    @classmethod
    def get_dsn(cls) -> str:
        self = cls()
        return "{}://{}:{}/{}".format(
            self.test_cache_driver,
            self.test_cache_host,
            self.test_cache_port,
            self.test_cache_db,
        )


class TestTopLevelConfig(BaseSettings):
    project_title_in: str = Field(validation_alias="project_title")
    db_dsn: str = Field(default_factory=TestDatabaseConfig.get_dsn)
    cache_dsn: str = Field(default_factory=TestCacheConfig.get_dsn)
    pubsub_dsn: str = Field(default_factory=TestPubsubConfig.get_dsn)

    @property
    def project_title(self) -> str:
        return f"Test {self.project_title_in}"


def get_top_config() -> TopLevelConfig:
    test_config = TestTopLevelConfig()
    return TopLevelConfig(
        log_level=LogLevel.debug,
        project_title=test_config.project_title,
        db_dsn=test_config.db_dsn,
        cache_dsn=test_config.cache_dsn,
        pubsub_dsn=test_config.pubsub_dsn,
    )
