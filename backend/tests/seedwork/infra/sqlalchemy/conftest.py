from collections.abc import AsyncIterator

import pytest

from tests.seedwork.confdata.container import SqlAlchemySeedWorkContainer
from tests.seedwork.confdata.infra.uow import (
    ITestUnitOfWork,
    IExampleRepository
)


@pytest.fixture(scope="function")
def sqlalchemy_seedwork_container():
    return SqlAlchemySeedWorkContainer()


@pytest.fixture(scope="function")
def uow(
    sqlalchemy_seedwork_container,
    _restart_example_table,
) -> ITestUnitOfWork:
    uow_factory = sqlalchemy_seedwork_container.uow_factory()
    return uow_factory()


@pytest.fixture(scope="function")
async def repo(uow: ITestUnitOfWork) -> AsyncIterator[IExampleRepository]:
    async with uow:
        yield uow.examples
