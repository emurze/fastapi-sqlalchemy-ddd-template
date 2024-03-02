import pytest

from shared.infra.in_memory.repository import InMemoryRepository
from shared.infra.in_memory.utils import id_int_gen
from shared.infra.in_memory.uow import InMemoryUnitOfWork
from tests.shared.domain.entities import Example
from tests.shared.domain.repository import IExampleRepository
from tests.shared.domain.uow import IExampleUnitOfWork


# Infra

class ExampleInMemoryRepository(InMemoryRepository, IExampleRepository):
    model = Example
    field_gens = {'id': id_int_gen}


class ExampleInMemoryUnitOfWork(InMemoryUnitOfWork, IExampleUnitOfWork):
    pass


# Container

@pytest.fixture
def repository() -> IExampleRepository:
    return ExampleInMemoryRepository()


@pytest.fixture
def uow() -> IExampleUnitOfWork:
    return ExampleInMemoryUnitOfWork(
        examples=ExampleInMemoryRepository,
    )
