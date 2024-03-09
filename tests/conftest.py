import pytest
from dependency_injector import providers

from main import app
from shared.infra.sqlalchemy_orm.base import base
from shared.infra.sqlalchemy_orm.common import suppress_echo
from collections.abc import Iterator, AsyncIterator, Callable

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.testclient import TestClient

from sqlalchemy import NullPool
from sqlalchemy.orm import clear_mappers
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from shared.presentation.container import create_container
from tests.config import test_db_dsn, TestTopLevelConfig


def get_engine():
    return create_async_engine(
        test_db_dsn, echo=True, poolclass=NullPool
    )


def get_session_factory(engine):
    return async_sessionmaker(engine, expire_on_commit=False)


db_engine = providers.Singleton(get_engine)
db_session_factory = providers.Singleton(get_session_factory, db_engine)

container = create_container(config=TestTopLevelConfig)
container.db_engine.override(db_engine)
container.db_session_factory.override(db_session_factory)

async_engine = container.db_engine()
async_session_factory = container.async_session_factory()


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
    Cleans tables before each test
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
    app.dependency_overrides[get_session_factory] = (  # noqa
        override_session_factory
    )

    with TestClient(app) as test_client:
        yield test_client
