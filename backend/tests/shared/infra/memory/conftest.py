import pytest

from shared.domain.repository import IGenericRepository
from tests.shared.conftest_data.domain import IExampleUnitOfWork
from tests.shared.conftest_data.repositories import (
    ExampleInMemoryRepository,
    ExampleInMemoryUnitOfWork,
)


@pytest.fixture(scope="function")
def repo() -> IGenericRepository:
    return ExampleInMemoryRepository()


@pytest.fixture(scope="function")
def uow() -> IExampleUnitOfWork:
    return ExampleInMemoryUnitOfWork(
        examples=ExampleInMemoryRepository,
    )
