from typing import Annotated

from fastapi import Depends

from auth.domain.uow import IAuthUnitOfWork
from auth.infra.repositories import in_memory


def uow() -> IAuthUnitOfWork:
    return in_memory.AuthInMemoryUnitOfWork(
        clients=in_memory.ClientInMemoryRepository,
    )


UoWDep = Annotated[IAuthUnitOfWork, Depends(uow)]
