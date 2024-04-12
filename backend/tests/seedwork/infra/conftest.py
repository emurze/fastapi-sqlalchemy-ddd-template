import pytest

from collections.abc import AsyncIterator
from typing import TypeAlias

from tests.seedwork.confdata import containers
from tests.seedwork.confdata.ports import ITestUnitOfWork, IExampleRepository

IterExampleRepo: TypeAlias = AsyncIterator[IExampleRepository]


@pytest.fixture(scope="function")
def sqlalchemy_uow(_restart_example_table) -> ITestUnitOfWork:
    container = containers.SqlAlchemySeedWorkContainer()
    return container.uow_factory()()


@pytest.fixture(scope="function")
def memory_uow() -> ITestUnitOfWork:
    container = containers.MemorySeedWorkContainer()
    return container.uow_factory()()


@pytest.fixture(scope="function")
async def sqlalchemy_repo(sqlalchemy_uow: ITestUnitOfWork) -> IterExampleRepo:
    async with sqlalchemy_uow:
        yield sqlalchemy_uow.examples


@pytest.fixture(scope="function")
async def memory_repo(memory_uow: ITestUnitOfWork) -> IterExampleRepo:
    async with memory_uow:
        yield memory_uow.examples

