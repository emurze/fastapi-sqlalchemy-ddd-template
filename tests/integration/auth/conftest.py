import pytest

from auth.domain.uow import IAuthUnitOfWork
from auth.infra import repositories as repos
from tests.shared.db import async_session_factory


@pytest.fixture
def uow() -> IAuthUnitOfWork:
    return repos.AuthSqlAlchemyUnitOfWork(
        session_factory=async_session_factory,
        clients=repos.ClientSqlAlchemyRepository,
    )
