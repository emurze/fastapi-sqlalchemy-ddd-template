import pytest
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import registry

from shared.domain.uow import IGenericUnitOfWork
from shared.infra.sqlalchemy_orm.common import suppress_echo
from shared.infra.sqlalchemy_orm.repository import SqlAlchemyRepository
from shared.infra.sqlalchemy_orm.uow import SqlAlchemyUnitOfWork
from tests.shared.db import async_engine, async_session_factory
from tests.shared.domain.entities import Example
from tests.shared.domain.repository import IExampleRepository
from tests.shared.domain.uow import IExampleUnitOfWork

# Infra

mapped_registry = registry()

example_table = sa.Table(
    "example",
    mapped_registry.metadata,
    sa.Column("id", sa.BIGINT, primary_key=True),
    sa.Column("name", sa.String, nullable=False),
)

mapped_registry.map_imperatively(Example, example_table)


class ExampleSqlAlchemyRepository(SqlAlchemyRepository, IExampleRepository):
    model = Example


class ExampleCachedAlchemyRepository(SqlAlchemyRepository, IExampleRepository):
    model = Example


class ExampleSqlAlchemyUnitOfWork(SqlAlchemyUnitOfWork, IExampleUnitOfWork):
    pass


# Container

@pytest.fixture(scope="function", autouse=True)
async def restart_example_table():
    async with async_engine.begin() as conn:
        async with suppress_echo(async_engine):
            await conn.run_sync(mapped_registry.metadata.drop_all)

        await conn.run_sync(mapped_registry.metadata.create_all)
        await conn.commit()


@pytest.fixture
def repository(session: AsyncSession) -> IExampleRepository:
    return ExampleSqlAlchemyRepository(session)


@pytest.fixture
def cached_repository(session: AsyncSession) -> IExampleRepository:
    return ExampleCachedAlchemyRepository(session)


@pytest.fixture
def uow() -> IGenericUnitOfWork:
    return ExampleSqlAlchemyUnitOfWork(
        session_factory=async_session_factory,
        examples=ExampleSqlAlchemyRepository,
    )
