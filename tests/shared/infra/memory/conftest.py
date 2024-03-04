import pytest

from shared.infra.memory.repository import InMemoryRepository
from shared.infra.memory.utils import id_int_gen
from shared.infra.memory.uow import InMemoryUnitOfWork
from tests.shared.conftest import (
    Example,
    IExampleRepository,
    IExampleUnitOfWork,
)


class ExampleInMemoryRepository(InMemoryRepository, IExampleRepository):
    model = Example
    field_gens = {'id': id_int_gen}


class ExampleInMemoryUnitOfWork(InMemoryUnitOfWork, IExampleUnitOfWork):
    pass


@pytest.fixture
def repo() -> IExampleRepository:
    return ExampleInMemoryRepository()


@pytest.fixture
def uow() -> IExampleUnitOfWork:
    return ExampleInMemoryUnitOfWork(
        examples=ExampleInMemoryRepository,
    )
