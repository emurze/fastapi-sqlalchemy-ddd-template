from pydantic import SecretStr
from pydantic_settings import BaseSettings


class DatabaseConfig(BaseSettings):
    db_name: str
    db_user: str
    db_pass: SecretStr
    db_host: str
    db_port: int

    def get_dsn(self, driver: str = "postgresql+asyncpg") -> str:
        return "{}://{}:{}@{}:{}/{}".format(
            driver,
            self.db_user,
            self.db_pass.get_secret_value(),
            self.db_host,
            self.db_port,
            self.db_name,
        )


db_config = DatabaseConfig()
