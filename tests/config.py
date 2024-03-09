from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings


class TestDatabaseConfig(BaseSettings):
    test_db_name: str
    test_db_user: str
    test_db_pass: SecretStr
    test_db_host: str
    test_db_port: int

    def get_dsn(self, driver: str = "postgresql+asyncpg") -> str:
        return "{}://{}:{}@{}:{}/{}".format(
            driver,
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

    def get_dsn(self, driver: str = "redis") -> str:
        return "{}://{}:{}/{}".format(
            driver,
            self.test_cache_host,
            self.test_cache_port,
            self.test_cache_db,
        )


test_cache_dsn = TestCacheConfig()
test_db_dsn = TestDatabaseConfig()


class TestTopLevelConfig(BaseSettings):
    secret_key: SecretStr
    project_title: str
    log_level: str
    db_dsn: str = Field(default_factory=test_cache_dsn.get_dsn)
    cache_dsn: str = Field(default_factory=test_db_dsn.get_dsn)


