import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from health.presentation.api import router as health_router

from container import container

config = container.config()
config.configure_logging()


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(
        config.cache_dsn,
        encoding=config.encoding,
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


lg = logging.getLogger(__name__)
app = FastAPI(
    docs_url=config.docs_url,
    redoc_url=config.redoc_url,
    title=config.title,
    version=config.version,
    secret_key=config.secret_key,
    config=config,
    lifespan=lifespan,
    container=container,
)
app.include_router(health_router)

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=config.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    extra_kw: dict = {}

    if config.debug:
        extra_kw["reload"] = True

    # todo: run this for production
    # gunicorn example:app -w 4 -k uvicorn.workers.UvicornWorker
    uvicorn.run(
        app="main:app",
        host=config.host,
        port=config.port,
        log_level=config.log_level,
        **extra_kw,
    )
