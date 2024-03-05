from auth.domain.uow import IAuthUnitOfWork
from auth.infra.repositories.sqlachemy import (
    AuthSqlAlchemyUnitOfWork,
    ClientSqlAlchemyRepository,
)
from tests.utils.core.integration import *  # noqa


@pytest.fixture
def uow() -> IAuthUnitOfWork:
    return AuthSqlAlchemyUnitOfWork(
        session_factory=async_session_factory,
        clients=ClientSqlAlchemyRepository,
    )
