from dependency_injector.providers import Singleton

from auth.infra.repositories import (
    AuthInMemoryUnitOfWork,
    ClientInMemoryRepository,
)
from post.infra.repositories import (
    PostInMemoryUnitOfWork,
    PostInMemoryRepository,
)
from container import AppContainer
from shared.infra.dependency_injector.utils import Link


def override_app_container(container, config, engine, session_factory) -> None:
    container.config.override(Link(config))
    container.db_engine.override(Link(engine))
    container.db_session_factory.override(Link(session_factory))


def get_memory_test_container() -> AppContainer:
    """
    Override infrastructure from SQLAlchemy to memory repositories
    and units of work
    """

    container = AppContainer()

    # Auth
    client_repo = Link(ClientInMemoryRepository)
    auth_uow = Singleton(AuthInMemoryUnitOfWork, clients=client_repo)
    container.client_repository.override(client_repo)
    container.auth_uow.override(auth_uow)

    # Post
    post_repo = Link(PostInMemoryRepository)
    post_uow = Singleton(PostInMemoryUnitOfWork, posts=post_repo)
    container.post_repository.override(post_repo)
    container.post_uow.override(post_uow)
    return container
