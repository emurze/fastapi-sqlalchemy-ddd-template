import pytest

from collections.abc import AsyncIterator
from typing import TypeAlias

from tests.seedwork.confdata import containers
from tests.seedwork.confdata.ports import ITestUnitOfWork, IExampleRepository

IteratorExampleRepo: TypeAlias = AsyncIterator[IExampleRepository]


@pytest.fixture(scope="function")
def sql_uow(_restart_example_table) -> ITestUnitOfWork:
    container = containers.SqlAlchemySeedWorkContainer()
    return container.uow_factory()()


@pytest.fixture(scope="function")
def mem_uow() -> ITestUnitOfWork:
    container = containers.get_memory_container()
    return container.uow_factory()()


@pytest.fixture(scope="function")
async def sql_repo(sql_uow: ITestUnitOfWork) -> IteratorExampleRepo:
    async with sql_uow:
        yield sql_uow.examples


@pytest.fixture(scope="function")
async def mem_repo(mem_uow: ITestUnitOfWork) -> IteratorExampleRepo:
    async with mem_uow:
        yield mem_uow.examples

