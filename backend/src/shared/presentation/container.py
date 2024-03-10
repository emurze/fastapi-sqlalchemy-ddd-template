import inspect
from collections.abc import Callable

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from auth.domain.uow import IAuthUnitOfWork
from auth.infra.repositories import AuthSqlAlchemyUnitOfWork, \
    ClientSqlAlchemyRepository
from post.application.command.create_post import CreatePostHandler
from post.application.command.delete_post import DeletePostHandler
from post.application.command.update_post import UpdatePostHandler
from post.application.query.get_post import GetPostHandler
from post.domain.repositories import IPostUnitOfWork
from post.infra.repositories import PostSqlAlchemyUnitOfWork, \
    PostSqlAlchemyRepository
from shared.application.message_bus import MessageBus
from shared.application.queries import IQueryHandler as IQHandler
from shared.application.commands import ICommandHandler as ICHandler
from shared.presentation.config import TopLevelConfig
from shared.presentation.message_bus import ProtectedMessageBus


def get_function_arguments(func: Callable):
    handler_signature = inspect.signature(func)
    kwargs_iterator = iter(handler_signature.parameters.items())
    _, first_param = next(kwargs_iterator)
    first_parameter = first_param.annotation

    remaining_parameters = {}
    for name, param in kwargs_iterator:
        remaining_parameters[name] = param.annotation

    return first_parameter, remaining_parameters


def get_config() -> TopLevelConfig:
    return TopLevelConfig()


def create_engine(config: TopLevelConfig) -> AsyncEngine:
    return create_async_engine(config.db_dsn, echo=True)


def create_session_factory(engine: AsyncEngine) -> Callable:
    return async_sessionmaker(engine)


def _register_handlers(register: Callable, handlers: list) -> None:
    for handler in handlers:
        command_or_query, _ = get_function_arguments(handler.handle)
        register(command_or_query, handler)


def create_bus(query_handlers: list, command_handlers: list) -> MessageBus:
    bus = ProtectedMessageBus()
    _register_handlers(bus.register_command_handler, command_handlers)
    _register_handlers(bus.register_query_handler, query_handlers)
    return bus


def group(*args) -> list:
    return list(args)


class AppContainer(containers.DeclarativeContainer):
    config = providers.Singleton(get_config)
    db_engine = providers.Singleton(create_engine, config)
    db_session_factory = providers.Singleton(create_session_factory, db_engine)

    # Auth
    auth_uow = providers.Singleton(
        AuthSqlAlchemyUnitOfWork,
        session_factory=db_session_factory,
        clients=ClientSqlAlchemyRepository,
    )

    # Post
    post_uow = providers.Singleton(
        PostSqlAlchemyUnitOfWork,
        session_factory=db_session_factory,
        posts=PostSqlAlchemyRepository,
    )
    get_post: IQHandler = providers.Singleton(GetPostHandler, post_uow)
    create_post: ICHandler = providers.Singleton(CreatePostHandler, post_uow)
    delete_post: ICHandler = providers.Singleton(DeletePostHandler, post_uow)
    update_post: ICHandler = providers.Singleton(UpdatePostHandler, post_uow)

    query_handlers = providers.Singleton(
        group,
        get_post,
    )
    command_handlers = providers.Singleton(
        group,
        create_post,
        delete_post,
        update_post,
    )
    message_bus = providers.Singleton(
        create_bus,
        query_handlers=query_handlers,
        command_handlers=command_handlers,
    )


container = AppContainer()
