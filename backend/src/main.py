from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqlalchemy.orm import clear_mappers

from health.presentation.api import router as health_router
from post.presentation.api import router as post_router

from container import container
from shared.infra.logging import configure_logging
from shared.infra.sqlalchemy_orm.base import base
from shared.presentation import exception_handlers as eh

config = container.config()


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


configure_logging()
app = FastAPI(
    title=config.project_title,
    lifespan=lifespan,
    secret_key=config.secret_key,
    container=container,
)
app.include_router(post_router)
app.include_router(health_router)

app.add_exception_handler(SystemError, eh.server_error_exception_handler)

origins = [
    "http://frontend:3000",
]
app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
