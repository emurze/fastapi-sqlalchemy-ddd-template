import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from seedwork.application.messagebus import MessageBus
from collections.abc import AsyncIterator
from typing import TypeAlias

from seedwork.domain.uows import IUnitOfWork
from seedwork.infra.database import suppress_echo
from seedwork.infra.database import Model
from tests.config import get_top_config
from tests.container import override_app_container, get_memory_test_container

from container import container as app_container
from redis import asyncio as aioredis

config = get_top_config()
engine = create_async_engine(config.db_dsn, echo=True, poolclass=NullPool)
session_factory = async_sessionmaker(engine, expire_on_commit=False)

override_app_container(app_container, config, engine, session_factory)
sqlalchemy_container: TypeAlias = app_container


@pytest.fixture(scope="function")
async def _restart_tables() -> None:
    """
    Cleans tables before each test.
    """
    async with engine.begin() as conn:
        async with suppress_echo(engine):
            await conn.run_sync(Model.metadata.drop_all)
            await conn.run_sync(Model.metadata.create_all)
        await conn.commit()


@pytest.fixture(scope="function")
async def _restart_cache() -> None:
    cache_conn = aioredis.Redis.from_url(config.cache_dsn)
    await cache_conn.flushdb(asynchronous=False)


@pytest.fixture(scope="function")
async def _restart_pubsub() -> None:
    cache_conn = aioredis.Redis.from_url(config.pubsub_dsn)
    await cache_conn.flushdb(asynchronous=False)


@pytest.fixture(scope="function")
def bus() -> MessageBus:
    memory_container = get_memory_test_container()
    return memory_container.message_bus()


@pytest.fixture(scope="function")
def memory_uow() -> IUnitOfWork:
    memory_container = get_memory_test_container()
    return memory_container.uow()


@pytest.fixture(scope="function")
def sqlalchemy_uow(_restart_tables) -> IUnitOfWork:
    return sqlalchemy_container.uow()


@pytest.fixture(scope="function")
async def ac(
    _restart_cache,
    _restart_pubsub,
    _restart_tables,
) -> AsyncIterator[AsyncClient]:
    """
    Provides a configured async test client for end-to-end tests.
    """
    from main import app

    async with LifespanManager(app) as manager:
        async with AsyncClient(app=manager.app, base_url="http://test") as ac:
            yield ac
