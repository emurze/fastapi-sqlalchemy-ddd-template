from pydantic import SecretStr
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


db_config = TestDatabaseConfig()
