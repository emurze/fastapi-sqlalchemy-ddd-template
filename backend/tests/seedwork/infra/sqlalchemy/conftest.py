import pytest

from tests.seedwork.confdata.container import SqlAlchemySeedWorkContainer
from tests.seedwork.confdata.uow import ISeedWorkUnitOfWork, IExampleRepository


@pytest.fixture(scope="function")
def sqlalchemy_seedwork_container():
    return SqlAlchemySeedWorkContainer()


@pytest.fixture(scope="function")
def uow(
    sqlalchemy_seedwork_container,
    _restart_example_table,
) -> ISeedWorkUnitOfWork:
    return sqlalchemy_seedwork_container.uow()


@pytest.fixture(scope="function")
async def repo(uow: ISeedWorkUnitOfWork) -> IExampleRepository:
    async with uow:
        yield uow.examples
