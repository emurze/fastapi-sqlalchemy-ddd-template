from collections.abc import Callable

from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

from auth.application import auth_module
from shared.presentation.config import TopLevelConfig
from shared.application import Application


def create_engine(config: dict) -> AsyncEngine:
    return create_async_engine(config["db_dsn"], echo=True)


def create_session_factory(engine: AsyncEngine) -> Callable:
    return async_sessionmaker(engine)


def create_application(config: dict, session_factory: Callable) -> Application:
    """
    Creates an instance of an application with the provided configuration
    and session factory.
    """

    application = Application(
        name=config["project_title"],
        session_factory=session_factory,
    )
    application.include_module(auth_module)
    return application


class TopLevelContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    db_engine = providers.Singleton(create_engine, config)
    db_session_factory = providers.Singleton(create_session_factory, db_engine)
    application = providers.Singleton(
        create_application, config, db_session_factory
    )


def create_container() -> TopLevelContainer:
    _config = TopLevelConfig()
    _container = TopLevelContainer()
    _container.config.from_dict(_config.model_dump())
    _container.config = TopLevelConfig(**_container.config())
    return _container


container = create_container()
