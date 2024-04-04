from dependency_injector import providers
from dependency_injector.providers import Factory

from auth.infra.repositories import AccountInMemoryRepository
from src.container import AppContainer
from seedwork.infra.injector import Link
from seedwork.infra.uows import InMemoryUnitOfWork


def override_app_container(container, config, engine, session_factory) -> None:
    container.config.override(Link(config))
    container.db_engine.override(Link(engine))
    container.db_session_factory.override(Link(session_factory))


def get_memory_container() -> AppContainer:
    """
    Override infrastructure from SQLAlchemy to memory repositories
    and units of work
    """

    container = AppContainer()
    container.uow.override(
        providers.Singleton(
            Factory,
            InMemoryUnitOfWork,
            accounts=AccountInMemoryRepository,
        )
    )
    return container
