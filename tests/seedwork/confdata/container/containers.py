from typing import Any, Callable

from dependency_injector import containers
from dependency_injector.providers import Factory, Singleton

from seedwork.application.messagebus import MessageBus
from seedwork.infra.injector import Link
from seedwork.infra.repository import as_memory
from seedwork.infra.uows import InMemoryUnitOfWork, SqlAlchemyUnitOfWork
from seedwork.presentation.factories import DictSingleton, HandlerSingleton
from tests.conftest import session_factory as db_session_factory
from tests.seedwork.confdata.application import command, query
from tests.seedwork.confdata.infra import repositories as repos


class SqlAlchemySeedWorkContainer(containers.DeclarativeContainer):
    session_factory = Link(db_session_factory)
    uow_factory: Any = Singleton(
        Factory,
        SqlAlchemyUnitOfWork,
        session_factory=session_factory,
        examples=repos.ExampleSqlAlchemyRepository,
    )
    query_handlers: Callable = DictSingleton(
        HandlerSingleton(query.get_example, session=session_factory),
        HandlerSingleton(query.get_example_item, session=session_factory),
    )
    command_handlers: Callable = DictSingleton(
        HandlerSingleton(command.create_example, uow=uow_factory),
        HandlerSingleton(command.update_example, uow=uow_factory),
        HandlerSingleton(command.delete_example, uow=uow_factory),
        HandlerSingleton(command.update_example_item, uow=uow_factory),
        HandlerSingleton(command.delete_example_item, uow=uow_factory),
    )
    event_handlers: Callable = DictSingleton()
    message_bus: Callable = Singleton(
        MessageBus,
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
            examples=as_memory(repos.ExampleSqlAlchemyRepository),
        )
    )
    return container


sql_container = SqlAlchemySeedWorkContainer()
