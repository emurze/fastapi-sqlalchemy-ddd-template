from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy.orm import clear_mappers

from auth.presentation.router import router as client_router
from shared.presentation.container import container

from shared.infra.sqlalchemy_orm.base import base


def include_routers(app_: FastAPI) -> None:
    app_.include_router(client_router)


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncIterator[None]:
    base.run_mappers()
    yield
    clear_mappers()


app = FastAPI(
    title=container.config.project_title,
    secrets=container.config.secret_key,
    lifespan=lifespan,
)
app.container = container
include_routers(app)
