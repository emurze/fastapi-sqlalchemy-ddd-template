from collections.abc import AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from shared.infra.sqlalchemy_orm.base import base
from shared.infra.sqlalchemy_orm.common import suppress_echo
from shared.test_deps import db
from shared.test_deps.db import async_engine


@pytest.fixture(scope="function", autouse=True)
async def restart_tables() -> None:
    """
    Cleans tables data before run test function
    """

    async with async_engine.begin() as conn:
        async with suppress_echo(async_engine):
            await conn.run_sync(base.metadata.drop_all)

        await conn.run_sync(base.metadata.create_all)
        await conn.commit()


@pytest.fixture(scope="function")
async def session() -> AsyncIterator[AsyncSession]:
    async with db.async_session_factory() as new_session:
        yield new_session


base.run_mappers()
