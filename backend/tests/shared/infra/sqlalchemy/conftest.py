from collections.abc import AsyncIterator, Callable
from typing import Iterator

import pytest
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession as ASession
from sqlalchemy.orm import registry, clear_mappers

from shared.domain.repository import IGenericRepository
from shared.domain.uow import IGenericUnitOfWork
from shared.infra.sqlalchemy_orm.common import suppress_echo
from shared.infra.sqlalchemy_orm.repository import SqlAlchemyRepository
from shared.infra.sqlalchemy_orm.uow import SqlAlchemyUnitOfWork
from tests.conftest import engine, session_factory
from tests.shared.conftest import Example, IExampleUnitOfWork

mapped_registry = registry()

example_table = sa.Table(
    "example",
    mapped_registry.metadata,
    sa.Column("id", sa.BIGINT, primary_key=True),
    sa.Column("name", sa.String, nullable=False),
)


def _run_example_mappers():
    mapped_registry.map_imperatively(Example, example_table)


class ExampleSqlAlchemyRepository(SqlAlchemyRepository, IGenericRepository):
    model = Example


class ExampleSqlAlchemyUnitOfWork(SqlAlchemyUnitOfWork, IExampleUnitOfWork):
    pass


# Built-in example fixtures

@pytest.fixture(scope="function")
def _example_mappers() -> Iterator[None]:
    _run_example_mappers()
    yield
    clear_mappers()


@pytest.fixture(scope="function")
async def _restart_example_table(_example_mappers) -> None:
    async with engine.begin() as conn:
        async with suppress_echo(engine):
            await conn.run_sync(mapped_registry.metadata.drop_all)
            await conn.run_sync(mapped_registry.metadata.create_all)
        await conn.commit()


@pytest.fixture(scope="function")
async def example_session(_restart_example_table) -> AsyncIterator[ASession]:
    async with session_factory() as new_session:
        yield new_session


@pytest.fixture(scope="function")
def example_session_factory(_restart_example_table) -> Callable:
    return session_factory


# Example fixtures

@pytest.fixture(scope="function")
def repo(example_session: ASession) -> IGenericRepository:
    return ExampleSqlAlchemyRepository(example_session)


@pytest.fixture(scope="function")
def uow(example_session_factory: Callable) -> IGenericUnitOfWork:
    return ExampleSqlAlchemyUnitOfWork(
        session_factory=example_session_factory,
        examples=ExampleSqlAlchemyRepository,
    )
