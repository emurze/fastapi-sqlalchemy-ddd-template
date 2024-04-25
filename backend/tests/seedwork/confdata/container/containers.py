from typing import Any, Callable

from dependency_injector import containers
from dependency_injector.providers import Factory, Singleton

from seedwork.infra.injector import Link
from seedwork.infra import repositories as generic_repos
from seedwork.infra.uows import InMemoryUnitOfWork, SqlAlchemyUnitOfWork
from seedwork.presentation.factories import get_dict, get_bus, get_handler
from tests.conftest import session_factory
from tests.seedwork.confdata.application import command, query
from tests.seedwork.confdata.infra import repositories as repos


class SqlAlchemySeedWorkContainer(containers.DeclarativeContainer):
    db_session_factory = Link(session_factory)
    uow_factory: Any = Singleton(
        Factory,
        SqlAlchemyUnitOfWork,
        session_factory=db_session_factory,
        examples={
            "command": repos.ExampleSqlAlchemyCommandRepository,
            "query": repos.ExampleSqlAlchemyQueryRepository,
        }
    )
    query_handlers: Callable = Singleton(
        get_dict,
        Singleton(get_handler, query.get_example, uow=uow_factory),
    )
    command_handlers: Callable = Singleton(
        get_dict,
        Singleton(get_handler, command.create_example, uow=uow_factory),
        Singleton(get_handler, command.update_example, uow=uow_factory),
        Singleton(get_handler, command.delete_example, uow=uow_factory),
    )
    event_handlers: Callable = Singleton(get_dict)
    message_bus: Callable = Singleton(
        get_bus,
        query_handlers=query_handlers,
        command_handlers=command_handlers,
        event_handlers=event_handlers,
    )


def get_memory_container():
    container = SqlAlchemySeedWorkContainer()
    container.uow_factory.override(
        Singleton(
            Singleton,
            InMemoryUnitOfWork,
            examples={
                "command": generic_repos.InMemoryCommandRepository,
                "query": repos.ExampleInMemoryQueryRepository,
            },
        )
    )
    return container


sql_container = SqlAlchemySeedWorkContainer()
