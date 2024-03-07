from pydantic import SecretStr
from pydantic_settings import BaseSettings


class TestDatabaseConfig(BaseSettings):
    test_db_name: str
    test_db_user: str
    test_db_pass: SecretStr
    test_db_host: str
    test_db_port: int

    @classmethod
    def get_dsn(cls, driver: str = "postgresql+asyncpg") -> str:
        self = cls()
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

    @classmethod
    def get_dsn(cls, driver: str = "redis") -> str:
        self = cls()
        return "{}://{}:{}/{}".format(
            driver,
            self.test_cache_host,
            self.test_cache_port,
            self.test_cache_db,
        )


test_cache_dsn = TestCacheConfig.get_dsn()
test_db_dsn = TestDatabaseConfig.get_dsn()
