import pytest

from main import app
from shared.infra.sqlalchemy_orm.base import base
from shared.infra.sqlalchemy_orm.common import suppress_echo
from shared.infra.sqlalchemy_orm.database import (
    get_session,  # Will be replaced by test dependency
    get_session_factory,  # Will be replaced by test dependency
)
from collections.abc import Iterator, AsyncIterator, Callable

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.testclient import TestClient

from sqlalchemy import NullPool
from sqlalchemy.orm import clear_mappers
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from tests.config import test_db_dsn

async_engine = create_async_engine(test_db_dsn, echo=True, poolclass=NullPool)
async_session_factory = async_sessionmaker(
    async_engine, expire_on_commit=False
)


@pytest.fixture(scope="function")
def _mappers() -> Iterator[None]:
    """
    Cleans and resets SQLAlchemy mapper configurations for each test.
    """
    base.run_mappers()
    yield
    clear_mappers()


@pytest.fixture(scope="function")
async def _restart_tables() -> None:
    """
    Clean tables before each test
    """
    async with async_engine.begin() as conn:
        async with suppress_echo(async_engine):
            await conn.run_sync(base.metadata.drop_all)
            await conn.run_sync(base.metadata.create_all)
        await conn.commit()


@pytest.fixture(scope="function")
def session_factory(_mappers, _restart_tables) -> Callable:
    """
    Provides session factory for each integration test (unit of work).
    """
    return async_session_factory


@pytest.fixture(scope="function")
async def session(_mappers, _restart_tables) -> AsyncIterator[AsyncSession]:
    """
    Provides session for each integration test (repository).
    """
    async with async_session_factory() as new_session:
        yield new_session


@pytest.fixture(scope="function")
def client(_restart_tables) -> Iterator[TestClient]:
    """
    Provides a configured test client for end-to-end tests.
    """

    def override_session_factory():
        return async_session_factory

    async def override_session() -> AsyncIterator[AsyncSession]:
        async with async_session_factory() as new_session:
            yield new_session

    app.dependency_overrides[get_session] = override_session  # noqa
    app.dependency_overrides[get_session_factory] = override_session_factory  # noqa

    with TestClient(app) as test_client:
        yield test_client
