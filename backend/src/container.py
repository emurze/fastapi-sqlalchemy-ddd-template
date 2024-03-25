from collections.abc import Callable

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
from blog.infra.repositories import PostSqlAlchemyRepository
from config import TopLevelConfig
from seedwork.application.messagebus import MessageBus
from seedwork.infra.functional import get_first_param_annotation
from seedwork.infra.injector import InjectIn, Group
from seedwork.infra.uows import SqlAlchemyUnitOfWork


def get_config() -> TopLevelConfig:
    return TopLevelConfig()


def get_engine(top_config: TopLevelConfig) -> AsyncEngine:
    return create_async_engine(top_config.db_dsn, echo=top_config.db_echo)


def get_session_factory(engine: AsyncEngine) -> Callable:
    return async_sessionmaker(engine)


def get_bus(
    query_handlers: list[tuple],
    command_handlers: list[tuple],
    event_handlers: list[tuple],
) -> MessageBus:
    return MessageBus(
        query_handlers={
            get_first_param_annotation(handler): wrapped
            for wrapped, handler in query_handlers
        },
        command_handlers={
            get_first_param_annotation(handler): wrapped
            for wrapped, handler in command_handlers
        },
        event_handlers={
            get_first_param_annotation(handler): wrapped
            for wrapped, handler in event_handlers
        },
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
    query_handlers = Group()
    command_handlers = Group(
        InjectIn(create_post_handler, uow),
        InjectIn(delete_post_handler, uow),
        InjectIn(update_post_handler, uow),
    )
    event_handlers = Group()
    message_bus = Singleton(
        get_bus, query_handlers, command_handlers, event_handlers
    )


container = AppContainer()
config = container.config()
