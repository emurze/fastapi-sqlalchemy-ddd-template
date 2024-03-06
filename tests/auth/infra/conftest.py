from collections.abc import Callable

import pytest

from auth.domain.uow import IAuthUnitOfWork
from auth.infra.repositories.sqlachemy import (
    AuthSqlAlchemyUnitOfWork,
    ClientSqlAlchemyRepository,
)


@pytest.fixture(scope="function")
def uow(session_factory: Callable) -> IAuthUnitOfWork:
    return AuthSqlAlchemyUnitOfWork(
        session_factory=session_factory,
        clients=ClientSqlAlchemyRepository,
    )
