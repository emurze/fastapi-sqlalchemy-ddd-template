from collections.abc import Callable

from dependency_injector import containers
from dependency_injector.providers import Singleton
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from auth.infra import repositories as auth_repos
from post.application.command.create_post import create_post_handler
from post.application.command.delete_post import delete_post_handler
from post.application.command.update_post import update_post_handler
from post.application.query.get_post import get_post_handler
from post.infra import repositories as post_repos
from config import TopLevelConfig
from shared.application.messagebus import MessageBus
from shared.infra.dependency_injector.utils import Link, Group, InjectIn
from shared.utils.functional import get_first_param_annotation


def get_config() -> TopLevelConfig:
    return TopLevelConfig()


def get_engine(config: TopLevelConfig) -> AsyncEngine:
    return create_async_engine(config.db_dsn, echo=True)


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
    client_repository = Link(auth_repos.ClientSqlAlchemyRepository)
    auth_uow = Singleton(
        auth_repos.AuthSqlAlchemyUnitOfWork,
        dsession_factory=db_session_factory,
        clients=client_repository,
    )
    post_repository = Link(post_repos.PostSqlAlchemyRepository)
    post_uow = Singleton(
        post_repos.PostSqlAlchemyUnitOfWork,
        session_factory=db_session_factory,
        posts=post_repository,
    )

    # Application
    query_handlers = Group(
        InjectIn(get_post_handler, post_uow),
    )
    command_handlers = Group(
        InjectIn(create_post_handler, post_uow),
        InjectIn(delete_post_handler, post_uow),
        InjectIn(update_post_handler, post_uow),
    )
    event_handlers = Group()
    message_bus = Singleton(
        get_bus, query_handlers, command_handlers, event_handlers
    )


container = AppContainer()
