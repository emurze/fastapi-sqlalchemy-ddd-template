from collections.abc import Callable
from typing import Annotated

from fastapi import Depends

from auth.domain.uow import IAuthUnitOfWork as IAUoW
from auth.infra.repositories.sqlachemy import (
    AuthSqlAlchemyUnitOfWork,
    ClientSqlAlchemyRepository,
)
from shared.infra.sqlalchemy_orm.database import get_session_factory


def uow(session_factory: Callable = Depends(get_session_factory)) -> IAUoW:
    return AuthSqlAlchemyUnitOfWork(
        session_factory=session_factory,
        clients=ClientSqlAlchemyRepository,
    )


UoWDep = Annotated[IAUoW, Depends(uow)]
