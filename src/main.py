from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.orm import clear_mappers

from config import app_config
from routers import include_routers

from shared.infra.sqlalchemy_orm.base import base


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncIterator[None]:
    base.run_mappers()
    yield
    clear_mappers()


app = FastAPI(
    title=app_config.project_title,
    secrets=app_config.secret_key,
    lifespan=lifespan,
)
include_routers(app)
