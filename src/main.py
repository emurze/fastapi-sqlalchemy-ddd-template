from fastapi import FastAPI

from config import app_config
from routers import include_routers

from shared.infra.sqlalchemy_orm.base import base

base.run_mappers()

app = FastAPI(
    title=app_config.project_title,
    secrets=app_config.secret_key,
)
include_routers(app)
