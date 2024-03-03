from typing import AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from shared.infra.sqlalchemy_orm.base import base
from shared.test_deps.db import async_session_factory


@pytest.fixture
async def session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as new_session:
        yield new_session


base.run_mappers()
