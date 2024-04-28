from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src.config import TopLevelConfig, LogLevel, generic_config


class TestDatabaseConfig(BaseSettings):
    model_config = generic_config
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
    model_config = generic_config
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
    model_config = generic_config
    test_title: str = "Test"
    test_log_level: str = LogLevel.info
    test_db_echo: bool = False
    test_db_dsn: str = Field(default_factory=TestDatabaseConfig.get_dsn)
    test_cache_dsn: str = Field(default_factory=TestCacheConfig.get_dsn)


def get_top_config() -> TopLevelConfig:
    test_config = TestTopLevelConfig()
    return TopLevelConfig(
        log_level=test_config.test_log_level,  # type: ignore
        title=test_config.test_title,
        db_dsn=test_config.test_db_dsn,
        db_echo=test_config.test_db_echo,
        cache_dsn=test_config.test_cache_dsn,
    )
