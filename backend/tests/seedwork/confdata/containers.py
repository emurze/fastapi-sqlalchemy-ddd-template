from typing import Any

from dependency_injector import containers
from dependency_injector.providers import Factory, Singleton

from seedwork.infra.injector import Link
from seedwork.infra.uows import InMemoryUnitOfWork, SqlAlchemyUnitOfWork
from tests.conftest import session_factory
from tests.seedwork.confdata import repositories as repos


class SqlAlchemySeedWorkContainer(containers.DeclarativeContainer):
    db_session_factory = Link(session_factory)
    uow_factory: Any = Singleton(
        Factory,
        SqlAlchemyUnitOfWork,
        session_factory=db_session_factory,
        examples=repos.ExampleSqlAlchemyRepository,
    )


class MemorySeedWorkContainer(containers.DeclarativeContainer):
    uow_factory: Any = Singleton(
        Factory,
        InMemoryUnitOfWork,
        examples=repos.ExampleInMemoryRepository,
    )
