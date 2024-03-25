import pytest

from seedwork.domain.repositories import IGenericRepository
from seedwork.domain.uows import IUnitOfWork
from seedwork.infra.uows import InMemoryUnitOfWork

from tests.shared.confdata.repositories import (
    ExampleInMemoryRepository,
)


@pytest.fixture(scope="function")
def repo() -> IGenericRepository:
    return ExampleInMemoryRepository()


@pytest.fixture(scope="function")
def uow() -> IUnitOfWork:
    return InMemoryUnitOfWork(examples=ExampleInMemoryRepository)
