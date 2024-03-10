from dependency_injector import providers

from auth.infra.repositories import (
    AuthInMemoryUnitOfWork,
    ClientInMemoryRepository,
)
from post.infra.repositories import (
    PostInMemoryUnitOfWork,
    PostInMemoryRepository,
)
from shared.presentation.container import AppContainer


def link(item):
    return providers.Singleton(lambda: item)


def override_app_container(container, config, engine, session_factory) -> None:
    container.config.override(link(config))
    container.db_engine.override(link(engine))
    container.db_session_factory.override(link(session_factory))


def get_memory_test_container() -> AppContainer:
    auth_uow = providers.Singleton(
        AuthInMemoryUnitOfWork,
        clients=ClientInMemoryRepository,
    )
    post_uow = providers.Singleton(
        PostInMemoryUnitOfWork,
        posts=PostInMemoryRepository,
    )
    container = AppContainer()
    container.auth_uow.override(auth_uow)
    container.post_uow.override(post_uow)
    return container


def get_sqlalchemy_test_container(
    config, engine, session_factory
) -> AppContainer:
    container = AppContainer()
    container.config.override(link(config))
    container.db_engine.override(link(engine))
    container.db_session_factory.override(link(session_factory))
    return container
