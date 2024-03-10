import inspect
from collections.abc import Callable

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from auth.infra.repositories import AuthSqlAlchemyUnitOfWork, \
    ClientSqlAlchemyRepository
from post.application.command.create_post import CreatePostHandler
from post.application.command.delete_post import DeletePostHandler
from post.application.command.update_post import UpdatePostHandler
from post.application.query.get_post import GetPostHandler
from post.infra.repositories import PostSqlAlchemyUnitOfWork, \
    PostSqlAlchemyRepository
from shared.application.message_bus import MessageBus
from config import TopLevelConfig


def _(obj, *args, **kw):
    return providers.Singleton(obj, *args, **kw)


def link(obj):
    return providers.Singleton(lambda: obj)


def group(*singletons):
    def inner(*args) -> list:
        return list(args)

    return providers.Singleton(inner, *singletons)


def get_first_param_annotation(func: Callable):
    handler_signature = inspect.signature(func)
    kwargs_iterator = iter(handler_signature.parameters.items())
    _, first_param = next(kwargs_iterator)
    return first_param.annotation


def get_config() -> TopLevelConfig:
    return TopLevelConfig()


def get_engine(config: TopLevelConfig) -> AsyncEngine:
    return create_async_engine(config.db_dsn, echo=True)


def get_session_factory(engine: AsyncEngine) -> Callable:
    return async_sessionmaker(engine)


def get_bus(query_handlers: list, command_handlers: list) -> MessageBus:
    return MessageBus(
        query_handlers={
            get_first_param_annotation(handler.handle): handler
            for handler in query_handlers
        },
        command_handlers={
            get_first_param_annotation(handler.handle): handler
            for handler in command_handlers
        }
    )


class AppContainer(containers.DeclarativeContainer):
    config = _(get_config)
    db_engine = _(get_engine, config)
    db_session_factory = _(get_session_factory, db_engine)

    client_repo = link(ClientSqlAlchemyRepository)
    auth_uow = _(
        AuthSqlAlchemyUnitOfWork,
        session_factory=db_session_factory,
        clients=client_repo,
    )
    post_repo = link(PostSqlAlchemyRepository)
    post_uow = _(
        PostSqlAlchemyUnitOfWork,
        session_factory=db_session_factory,
        posts=post_repo,
    )

    query_handlers = group(
        _(GetPostHandler, post_uow),
    )
    command_handlers = group(
        _(CreatePostHandler, post_uow),
        _(DeletePostHandler, post_uow),
        _(UpdatePostHandler, post_uow),
    )
    message_bus = _(get_bus, query_handlers, command_handlers)


container = AppContainer()
