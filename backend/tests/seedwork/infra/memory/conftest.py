from collections.abc import AsyncIterator

import pytest

from tests.seedwork.confdata.container import MemorySeedWorkContainer
from tests.seedwork.confdata.infra.uow import (
    ITestUnitOfWork,
    IExampleRepository,
)


@pytest.fixture(scope="function")
def memory_seedwork_container():
    return MemorySeedWorkContainer()


@pytest.fixture(scope="function")
def uow(memory_seedwork_container) -> ITestUnitOfWork:
    uow_factory = memory_seedwork_container.uow_factory()
    return uow_factory()


@pytest.fixture(scope="function")
async def repo(uow: ITestUnitOfWork) -> AsyncIterator[IExampleRepository]:
    async with uow:
        yield uow.examples
