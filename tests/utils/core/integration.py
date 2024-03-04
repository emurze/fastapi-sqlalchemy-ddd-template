from collections.abc import AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from shared.infra.sqlalchemy_orm.base import base
from tests.utils.core import utils
from tests.utils.db import async_session_factory


@pytest.fixture(scope="function", autouse=True)
async def restart_tables() -> None:
    """
    Cleans tables data before run test function
    """
    await utils.restart_tables()


@pytest.fixture(scope="function")
async def session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as new_session:
        yield new_session


base.run_mappers()
