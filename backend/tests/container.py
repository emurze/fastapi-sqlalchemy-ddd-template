from dependency_injector.providers import Singleton

from blog.infra.repositories import PostInMemoryRepository
from container import AppContainer
from seedwork.infra.injector import Link
from seedwork.infra.uows import InMemoryUnitOfWork


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
    uow = Singleton(
        InMemoryUnitOfWork,
        posts=PostInMemoryRepository,
    )
    container.uow.override(uow)
    return container
