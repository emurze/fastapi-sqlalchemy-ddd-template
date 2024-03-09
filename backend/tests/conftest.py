import pytest
from dependency_injector import providers

from shared.infra.sqlalchemy_orm.base import base
from shared.infra.sqlalchemy_orm.common import suppress_echo
from collections.abc import Iterator, AsyncIterator, Callable

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from starlette.testclient import TestClient

from sqlalchemy import NullPool
from sqlalchemy.orm import clear_mappers
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from shared.presentation.container import container
from backend.tests.config import TestTopLevelConfig


def get_engine(config: TestTopLevelConfig) -> AsyncEngine:
    return create_async_engine(config.db_dsn, echo=True, poolclass=NullPool)


def get_session_factory(engine) -> Callable:
    return async_sessionmaker(engine, expire_on_commit=False)


class TestContainer:
    """
    A container for overriding default dependencies during testing.
    """

    config = providers.Singleton(TestTopLevelConfig)
    db_engine = providers.Singleton(get_engine, config)
    db_session_factory = providers.Singleton(get_session_factory, db_engine)

    def override_dependencies(self):
        container.config.override(self.config)
        container.db_engine.override(self.db_engine)
        container.db_session_factory.override(self.db_session_factory)


test_container = TestContainer()
test_container.override_dependencies()

from main import app  # noqa imports app with overridden container


async_engine = container.db_engine()
async_session_factory = container.db_session_factory()


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
    with TestClient(app) as test_client:
        yield test_client
