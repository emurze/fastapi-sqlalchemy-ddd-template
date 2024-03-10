import pytest

from shared.domain.repository import IGenericRepository
from shared.infra.memory.repository import InMemoryRepository
from shared.infra.memory.utils import id_int_gen
from shared.infra.memory.uow import InMemoryUnitOfWork
from tests.shared.conftest import Example, IExampleUnitOfWork


class ExampleInMemoryRepository(InMemoryRepository, IGenericRepository):
    model = Example
    field_gens = {"id": id_int_gen}


class ExampleInMemoryUnitOfWork(InMemoryUnitOfWork, IExampleUnitOfWork):
    pass


@pytest.fixture(scope="function")
def repo() -> IGenericRepository:
    return ExampleInMemoryRepository()


@pytest.fixture(scope="function")
def uow() -> IExampleUnitOfWork:
    return ExampleInMemoryUnitOfWork(examples=ExampleInMemoryRepository)
