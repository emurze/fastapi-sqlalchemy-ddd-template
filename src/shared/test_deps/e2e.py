import pytest

from main import app
from shared.infra.sqlalchemy_orm.base import base
from shared.infra.sqlalchemy_orm.common import suppress_echo
from shared.infra.sqlalchemy_orm.database import get_session, async_engine
from collections.abc import Iterator, AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.testclient import TestClient

from shared.test_deps.db import async_session_factory


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
def client() -> Iterator[TestClient]:
    """
    Overrides the normal database access with test database,
    and yields a configured test client
    """

    async def override_session() -> AsyncIterator[AsyncSession]:
        async with async_session_factory() as new_session:
            yield new_session

    app.dependency_overrides[get_session] = override_session  # noqa

    with TestClient(app) as test_client:
        yield test_client
