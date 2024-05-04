from collections.abc import Callable
from typing import Any

from dependency_injector import containers
from dependency_injector.providers import Singleton, Factory
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from seedwork.application.messagebus import MessageBus
from src.config import TopLevelConfig
from seedwork.infra.uows import SqlAlchemyUnitOfWork
from seedwork.presentation.factories import DictSingleton


def get_engine(top_config: TopLevelConfig) -> AsyncEngine:
    return create_async_engine(
        top_config.db_dsn,
        echo=top_config.db_echo,
        pool_size=top_config.pool_size,
        max_overflow=top_config.pool_max_overflow,
    )


def get_session_factory(engine: AsyncEngine) -> Callable:
    return async_sessionmaker(engine)


class AppContainer(containers.DeclarativeContainer):
    config: Any = Singleton(TopLevelConfig)
    db_engine = Singleton(get_engine, config)
    db_session_factory = Singleton(get_session_factory, db_engine)
    uow: Any = Singleton(
        Factory,
        SqlAlchemyUnitOfWork,
        session_factory=db_session_factory,
    )
    query_handlers: Callable = DictSingleton()
    command_handlers: Callable = DictSingleton()
    event_handlers: Callable = DictSingleton()
    message_bus: Callable = Singleton(
        MessageBus,
        query_handlers=query_handlers,
        command_handlers=command_handlers,
        event_handlers=event_handlers,
    )


container = AppContainer()
