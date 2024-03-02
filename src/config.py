from pydantic import SecretStr
from pydantic_settings import BaseSettings


class AppConfig(BaseSettings):
    secret_key: SecretStr
    project_title: str
    log_level: str


app_config = AppConfig()
