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
from blog.presentation.api import router as post_router

from container import container, config
from seedwork.infra.logging import configure_logging
from seedwork.presentation import exception_handlers as eh


@asynccontextmanager
async def lifespan(app_: FastAPI) -> AsyncIterator[None]:
    configure_logging(config.log_level)
    redis = aioredis.from_url(
        config.cache_dsn,
        encoding="utf8",
        decode_responses=True,
    )
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


lg = logging.getLogger(__name__)
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


if __name__ == '__main__':
    extra_kw = {}

    if config.debug:
        extra_kw["reload"] = True

    uvicorn.run(
        app="main:app",
        host=config.host,
        port=config.port,
        log_level=config.log_level,
        **extra_kw,
    )
