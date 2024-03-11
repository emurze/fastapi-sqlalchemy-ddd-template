from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqlalchemy.orm import clear_mappers

from auth.presentation.router import router as auth_router
from health.presentation.router import router as health_router
from post.presentation.router import router as post_router

from container import container
from shared.infra.sqlalchemy_orm.base import base

config = container.config()


def include_routers(app_: FastAPI) -> None:
    app_.include_router(auth_router)
    app_.include_router(post_router)
    app_.include_router(health_router)


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(
        config.cache_dsn,
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    base.run_mappers()
    yield
    clear_mappers()


app = FastAPI(
    title=config.project_title,
    lifespan=lifespan,
    secret_key=config.secret_key,
    container=container,
)
include_routers(app)
