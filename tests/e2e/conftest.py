from main import app
from shared.infra.sqlalchemy_orm.database import get_session
from collections.abc import Iterator, AsyncIterator

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.testclient import TestClient

from tests.shared import db


@pytest.fixture(scope="function", autouse=True)
async def restart_tables() -> None:
    await db.restart_tables()


@pytest.fixture(scope="function")
def client() -> Iterator[TestClient]:
    """
    Overrides the normal database access with test database,
    and yields a configured test client
    """

    async def override_session() -> AsyncIterator[AsyncSession]:
        async with db.async_session_factory() as new_session:
            yield new_session

    app.dependency_overrides[get_session] = override_session  # noqa

    with TestClient(app) as test_client:
        yield test_client
