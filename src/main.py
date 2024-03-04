from pprint import pprint

from fastapi import FastAPI, Depends
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from config import app_config
from routers import include_routers
from shared.infra.redis.cache.config import get_cache_dsn

from redis import asyncio as aioredis

from shared.infra.sqlalchemy_orm.base import base

app = FastAPI(
    title=app_config.project_title,
    secrets=app_config.secret_key,
)
include_routers(app)


@app.on_event("startup")
async def startup_event(cache_dsn: str = Depends(get_cache_dsn)):
    base.run_mappers()
    # print(cache_dsn)
    # dsn = cache_dsn.dependency()
    # redis = aioredis.from_url(
    #     cache_dsn,
    #     encoding="utf8",
    #     decode_responses=True,
    # )
    # FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
