import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from seedwork.application.messagebus import MessageBus
from collections.abc import Iterator, AsyncIterator

from starlette.testclient import TestClient

from seedwork.infra.database import suppress_echo
from seedwork.infra.database import Model
from tests.config import get_top_config
from tests import container as co

from container import container as app_container
from redis import asyncio as aioredis

config = get_top_config()
engine = create_async_engine(config.db_dsn, echo=True, poolclass=NullPool)
session_factory = async_sessionmaker(engine, expire_on_commit=False)

co.override_app_container(app_container, config, engine, session_factory)


# Cleaners


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


# Application fixtures


@pytest.fixture(scope="function")
def bus() -> MessageBus:
    """
    Fixture for Application tests.
    """
    memory_container = co.get_memory_test_container()
    return memory_container.message_bus()


# Infrastructure fixtures


@pytest.fixture(scope="function")
def sqlalchemy_container(_restart_tables):
    """
    Provides sqlalchemy repositories and units of work.
    """
    return app_container


@pytest.fixture(scope="function")
def memory_container():
    """
    Provides memory repositories and units of work.
    """
    return co.get_memory_test_container()


@pytest.fixture(scope="function")
async def session() -> AsyncIterator[AsyncSession]:
    """
    This session is typically injected into repository classes for performing
    database operations.
    """
    async with session_factory() as new_session:
        yield new_session


# End To End fixtures


@pytest.fixture(scope="function")
async def ac(_restart_cache, _restart_tables) -> Iterator[TestClient]:
    """
    Provides a configured async test client for end-to-end tests.
    """
    from main import app

    async with LifespanManager(app) as manager:
        async with AsyncClient(app=manager.app, base_url="http://test") as ac:
            yield ac
