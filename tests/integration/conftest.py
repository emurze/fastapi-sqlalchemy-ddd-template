from collections.abc import AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from shared.infra.sqlalchemy_orm.base import base

from tests.shared import db


@pytest.fixture(scope="function", autouse=True)
async def restart_tables() -> None:
    await db.restart_tables()


@pytest.fixture(scope="function")
async def session() -> AsyncIterator[AsyncSession]:
    async with db.async_session_factory() as session:
        yield session


base.run_mappers()
