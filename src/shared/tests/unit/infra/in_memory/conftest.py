import pytest

from shared.infra.in_memory.repository import InMemoryRepository
from shared.infra.in_memory.utils import id_int_gen
from shared.infra.in_memory.uow import InMemoryUnitOfWork
from shared.tests.shared.conftest import (
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
def repository() -> IExampleRepository:
    return ExampleInMemoryRepository()


@pytest.fixture
def uow() -> IExampleUnitOfWork:
    return ExampleInMemoryUnitOfWork(
        examples=ExampleInMemoryRepository,
    )
