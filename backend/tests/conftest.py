import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from shared.application.message_bus import MessageBus
from shared.infra.sqlalchemy_orm.base import base
from shared.infra.sqlalchemy_orm.common import suppress_echo
from collections.abc import Iterator

from starlette.testclient import TestClient

from sqlalchemy.orm import clear_mappers

from tests.config import TestTopLevelConfig
from tests import containers as co

from shared.presentation.container import container

# Initialize test configuration
config = TestTopLevelConfig()

# Create Asyncio SQLAlchemy engine and session factory
engine = create_async_engine(config.db_dsn, echo=True, poolclass=NullPool)
session_factory = async_sessionmaker(engine, expire_on_commit=False)

# Override app container with test configurations
co.override_app_container(container, config, engine, session_factory)

# Obtain test containers for memory and SQLAlchemy configurations
# providing ??? tailored ??? handlers for efficient testing.
memory_container = co.get_memory_test_container()
sqlalchemy_container = co.get_sqlalchemy_test_container(
    config=config,
    engine=engine,
    session_factory=session_factory,
)


@pytest.fixture(scope="function")
async def _restart_tables() -> None:
    """
    Cleans tables before each test
    """
    async with engine.begin() as conn:
        async with suppress_echo(engine):
            await conn.run_sync(base.metadata.drop_all)
            await conn.run_sync(base.metadata.create_all)
        await conn.commit()


@pytest.fixture(scope="function")
def _mappers() -> Iterator[None]:
    """
    Cleans and resets SQLAlchemy mapper configurations for each test.
    """
    base.run_mappers()
    yield
    clear_mappers()


@pytest.fixture(scope="function")
def sqlalchemy_bus(_mappers, _restart_tables) -> MessageBus:
    """
    Fixture for SQLAlchemy message bus.
    """
    return sqlalchemy_container.message_bus()


@pytest.fixture(scope="function")
def memory_bus() -> MessageBus:
    """
    Fixture for memory message bus.
    """
    return memory_container.message_bus()


@pytest.fixture(scope="function")
def client(_restart_tables) -> Iterator[TestClient]:
    """
    Provides a configured test client for end-to-end tests.
    """
    from main import app

    with TestClient(app) as test_client:
        yield test_client
