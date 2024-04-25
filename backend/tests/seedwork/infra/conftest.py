import pytest

from tests.seedwork.confdata.container import containers
from tests.seedwork.confdata.domain.ports import ITestUnitOfWork


@pytest.fixture(scope="function")
def sql_uow(_restart_example_table) -> ITestUnitOfWork:
    container = containers.SqlAlchemySeedWorkContainer()
    return container.uow_factory()()


@pytest.fixture(scope="function")
def mem_uow() -> ITestUnitOfWork:
    container = containers.get_memory_container()
    return container.uow_factory()()
