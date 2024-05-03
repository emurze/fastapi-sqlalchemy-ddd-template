from collections.abc import Iterator

import pytest

from seedwork.application.messagebus import MessageBus
from seedwork.domain.repositories import IGenericRepository
from seedwork.infra.database import suppress_echo
from seedwork.infra.repository import InMemoryRepository, raise_loading_errors
from tests.conftest import engine
from tests.seedwork.confdata.container import containers
from tests.seedwork.confdata.domain.entities import Example
from tests.seedwork.confdata.domain.ports import ITestUnitOfWork
from tests.seedwork.confdata.infra.models import Model, start_mappers


@pytest.fixture(scope="session", autouse=True)
async def _start_mappers() -> None:
    start_mappers()


@pytest.fixture(scope="function")
async def _restart_example_table() -> None:
    async with engine.begin() as conn:
        with suppress_echo(engine):
            await conn.run_sync(Model.metadata.drop_all)
            await conn.run_sync(Model.metadata.create_all)
        await conn.commit()


@pytest.fixture(scope="function")
def sql_uow(_restart_example_table) -> ITestUnitOfWork:
    container = containers.SqlAlchemySeedWorkContainer()
    return container.uow_factory()()


@pytest.fixture(scope="function")
def mem_uow() -> ITestUnitOfWork:
    container = containers.get_memory_container()
    return container.uow_factory()()


@pytest.fixture(scope="function")
def sql_bus(_restart_example_table) -> MessageBus:
    return containers.sql_container.message_bus()


@pytest.fixture(scope="function")
def mem_bus() -> MessageBus:
    memory_container = containers.get_memory_container()
    return memory_container.message_bus()


@pytest.fixture(scope="function")
def mem_examples() -> Iterator[IGenericRepository]:
    repository = InMemoryRepository(Example)
    with raise_loading_errors(repository):
        yield repository
