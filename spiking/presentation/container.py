from typing import Any

from dependency_injector.providers import Singleton, Factory
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
)
from sqlalchemy.orm import DeclarativeBase

from seedwork.application.messagebus import MessageBus
from seedwork.infra.uows import SqlAlchemyUnitOfWork
from seedwork.presentation.factories import DictSingleton, HandlerSingleton, \
    EventListSingleton
from spiking.application.create_post import create_post
from spiking.application.get_post import get_post
from spiking.application.when_post_created import print_hello, \
    publish_post
from spiking.application.when_post_populated import update_author
from spiking.application.when_post_published import populate_post
from spiking.infra.repositories import PostSqlAlchemyRepository


def get_engine():
    return create_async_engine(
        "postgresql+asyncpg://test_adm1:12345678@localhost:5432/test_learning",
        echo=True,
    )


def get_session_factory(engine: AsyncEngine):
    return async_sessionmaker(engine, expire_on_commit=False)


class Container(DeclarativeBase):
    engine = Singleton(get_engine)
    session_factory = Singleton(get_session_factory, engine)
    uow_factory: Any = Singleton(
        Factory,
        SqlAlchemyUnitOfWork,
        session_factory=session_factory,
        posts=PostSqlAlchemyRepository,
    )
    command_handlers = DictSingleton(
        HandlerSingleton(create_post, uow=uow_factory),
    )
    query_handlers = DictSingleton(
        HandlerSingleton(get_post, session=session_factory),
    )
    event_handlers = EventListSingleton(
        HandlerSingleton(print_hello),
        HandlerSingleton(publish_post, uow=True),
        HandlerSingleton(populate_post, uow=True),
        HandlerSingleton(update_author, uow=True),
    )
    messagebus = Singleton(
        MessageBus,
        command_handlers=command_handlers,
        query_handlers=query_handlers,
        event_handlers=event_handlers,
    )
