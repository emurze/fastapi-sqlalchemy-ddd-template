from collections.abc import Callable
from typing import TypeAlias

from dependency_injector import containers
from dependency_injector.providers import Singleton
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from blog.application.command.create_post import create_post_handler
from blog.application.command.delete_post import delete_post_handler
from blog.application.command.update_post import update_post_handler
from blog.application.event.notify_developers import notify_developers
from blog.infra.repositories import PostSqlAlchemyRepository
from config import TopLevelConfig
from seedwork.application.messagebus import MessageBus, Message
from seedwork.domain.uows import IUnitOfWork
from seedwork.infra.functional import get_first_param_type
from seedwork.infra.uows import SqlAlchemyUnitOfWork

WrappedHandler: TypeAlias = Callable


def get_handler(handler, *args, **kw) -> dict[type[Message], WrappedHandler]:
    def wrapper(message):
        return handler(message, *args, **kw)
    return {get_first_param_type(handler): wrapper}


def get_dict(*handlers: dict) -> dict[type[Message], WrappedHandler]:
    return {k: v for handler in handlers for k, v in handler.items()}


def get_config() -> TopLevelConfig:
    return TopLevelConfig()


def get_engine(top_config: TopLevelConfig) -> AsyncEngine:
    return create_async_engine(top_config.db_dsn, echo=top_config.db_echo)


def get_session_factory(engine: AsyncEngine) -> Callable:
    return async_sessionmaker(engine)


def get_bus(
    uow: IUnitOfWork,
    query_handlers: dict[type[Message], WrappedHandler],
    command_handlers: dict[type[Message], WrappedHandler],
    event_handlers: dict[type[Message], WrappedHandler],
) -> MessageBus:
    return MessageBus(
        uow=uow,
        query_handlers=query_handlers,
        command_handlers=command_handlers,
        event_handlers=event_handlers,
    )


class AppContainer(containers.DeclarativeContainer):
    config = Singleton(get_config)
    db_engine = Singleton(get_engine, config)
    db_session_factory = Singleton(get_session_factory, db_engine)

    # Infrastructure
    uow = Singleton(
        SqlAlchemyUnitOfWork,
        session_factory=db_session_factory,
        posts=PostSqlAlchemyRepository,
    )

    # Application
    query_handlers = Singleton(get_dict)
    command_handlers = Singleton(
        get_dict,
        Singleton(get_handler, create_post_handler, uow=uow),
        Singleton(get_handler, update_post_handler, uow=uow),
        Singleton(get_handler, delete_post_handler, uow=uow)
    )
    event_handlers = Singleton(
        get_dict,
        Singleton(get_handler, notify_developers),
    )
    message_bus = Singleton(
        get_bus,
        uow=uow,
        query_handlers=query_handlers,
        command_handlers=command_handlers,
        event_handlers=event_handlers,
    )


container = AppContainer()
