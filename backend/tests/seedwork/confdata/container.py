from typing import Any

from dependency_injector import containers
from dependency_injector.providers import Factory

from seedwork.infra.injector import Link
from seedwork.infra.uows import InMemoryUnitOfWork, SqlAlchemyUnitOfWork
from tests.conftest import session_factory
from tests.seedwork.confdata.repositories import (
    ExampleInMemoryRepository,
    ExampleSqlAlchemyRepository,
)


class SqlAlchemySeedWorkContainer(containers.DeclarativeContainer):
    db_session_factory = Link(session_factory)
    uow: Any = Factory(
        Factory,
        SqlAlchemyUnitOfWork,
        session_factory=db_session_factory,
        examples=ExampleSqlAlchemyRepository,
    )


class MemorySeedWorkContainer(containers.DeclarativeContainer):
    uow: Any = Factory(
        Factory,
        InMemoryUnitOfWork,
        examples=ExampleInMemoryRepository,
    )
