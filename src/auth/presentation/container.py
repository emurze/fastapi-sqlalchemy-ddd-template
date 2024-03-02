from fastapi import Depends

from auth.application.command.add_client import AddClientHandler
from auth.domain.uow import IAuthUnitOfWork
from auth.infra.repositories import in_memory


def auth_uow() -> IAuthUnitOfWork:
    return in_memory.AuthInMemoryUnitOfWork(
        clients=in_memory.ClientInMemoryRepository,
    )


def get_client_query_handler(uow: IAuthUnitOfWork = Depends(auth_uow)):
    return AddClientHandler()
