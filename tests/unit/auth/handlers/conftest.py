import pytest

from auth.application.command.add_client import (
    AddClientHandler,
    AddClientCommand,
    AddClientResult,
)
from auth.domain.uow import IAuthUnitOfWork
from auth.infra.repositories import in_memory


async def make_client(uow: IAuthUnitOfWork, **kw) -> AddClientResult:
    handler = AddClientHandler(uow)
    command = AddClientCommand(**kw)
    return await handler.execute(command)


@pytest.fixture
def uow() -> IAuthUnitOfWork:
    return in_memory.AuthInMemoryUnitOfWork(
        clients=in_memory.ClientInMemoryRepository,
    )
