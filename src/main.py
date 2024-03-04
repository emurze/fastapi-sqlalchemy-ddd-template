from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from config import app_config
from routers import include_routers
from shared.infra.redis.cache.config import cache_config

from redis import asyncio as aioredis

from shared.infra.sqlalchemy_orm.base import base


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator:
    # Inject redis test db
    base.run_mappers()
    redis = aioredis.from_url(
        cache_config.get_dsn(),
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(
    title=app_config.project_title,
    secrets=app_config.secret_key,
    lifespan=lifespan,
)
include_routers(app)
