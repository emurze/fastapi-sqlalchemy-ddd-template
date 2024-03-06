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


@pytest.fixture(scope="function")
def repo() -> IExampleRepository:
    """
    Every test it returns a new repository with cleaned models
    """

    return ExampleInMemoryRepository()


@pytest.fixture(scope="function")
def uow() -> IExampleUnitOfWork:
    """
    Every test it returns a new uow with repositories with cleaned models
    """

    return ExampleInMemoryUnitOfWork(examples=ExampleInMemoryRepository)
