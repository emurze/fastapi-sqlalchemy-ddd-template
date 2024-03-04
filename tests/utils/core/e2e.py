import pytest

from main import app
from shared.infra.sqlalchemy_orm.database import get_session, \
    get_session_factory
from collections.abc import Iterator, AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.testclient import TestClient

from tests.utils.db import async_session_factory
from tests.utils.core import utils


@pytest.fixture(scope="function", autouse=True)
async def restart_tables() -> None:
    """
    Cleans tables data before run test function
    """
    await utils.restart_tables()


@pytest.fixture(scope="function")
def client() -> Iterator[TestClient]:
    """
    Overrides the normal database access with test database,
    and yields a configured test client
    """

    def override_session_factory():
        return async_session_factory

    async def override_session() -> AsyncIterator[AsyncSession]:
        async with async_session_factory() as new_session:
            yield new_session

    app.dependency_overrides[get_session] = override_session  # noqa
    app.dependency_overrides[get_session_factory] = override_session_factory  # noqa

    with TestClient(app) as test_client:
        yield test_client
