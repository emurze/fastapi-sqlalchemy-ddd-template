from auth.infra.repositories import (
    AuthInMemoryUnitOfWork,
    ClientInMemoryRepository,
)
from post.infra.repositories import (
    PostInMemoryUnitOfWork,
    PostInMemoryRepository,
)
from containers import AppContainer, link, _


def override_app_container(container, config, engine, session_factory) -> None:
    container.config.override(link(config))
    container.db_engine.override(link(engine))
    container.db_session_factory.override(link(session_factory))


def get_memory_test_container() -> AppContainer:
    container = AppContainer()

    # Auth
    client_repo = link(ClientInMemoryRepository)
    auth_uow = _(AuthInMemoryUnitOfWork, clients=client_repo)
    container.client_repo.override(client_repo)
    container.auth_uow.override(auth_uow)

    # Post
    post_repo = link(PostInMemoryRepository)
    post_uow = _(PostInMemoryUnitOfWork, posts=post_repo)
    container.post_repo.override(post_repo)
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
