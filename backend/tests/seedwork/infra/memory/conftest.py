import pytest

from tests.seedwork.confdata.container import MemorySeedWorkContainer
from tests.seedwork.confdata.uow import ISeedWorkUnitOfWork, IExampleRepository


@pytest.fixture(scope="function")
def memory_seedwork_container():
    return MemorySeedWorkContainer()


@pytest.fixture(scope="function")
def uow(memory_seedwork_container) -> ISeedWorkUnitOfWork:
    return memory_seedwork_container.uow()


@pytest.fixture(scope="function")
def repo(uow: ISeedWorkUnitOfWork) -> IExampleRepository:
    print(f"UOW {uow=}")
    return uow.examples
