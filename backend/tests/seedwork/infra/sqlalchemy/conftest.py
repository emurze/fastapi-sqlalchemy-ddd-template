import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.domain.repositories import IGenericRepository
from tests.conftest import session_factory
from tests.shared.confdata.entities import IExampleUnitOfWork
from tests.shared.confdata.repositories import (
    ExampleSqlAlchemyUnitOfWork,
    ExampleSqlAlchemyRepository,
)


@pytest.fixture(scope="function")
def repo(session: AsyncSession, _restart_example_table) -> IGenericRepository:
    return ExampleSqlAlchemyRepository(session)


@pytest.fixture(scope="function")
def uow(_restart_example_table) -> IExampleUnitOfWork:
    return ExampleSqlAlchemyUnitOfWork(
        session_factory=session_factory,
        examples=ExampleSqlAlchemyRepository,
    )
