import pytest

from auth.application.command_handlers.add_client import AddClientHandler
from auth.application.commands.add_client import (
    AddClientCommand,
    AddClientPayload,
)
from auth.domain.uow import IAuthUnitOfWork
from auth.infra.repositories import memory


async def make_client(uow: IAuthUnitOfWork, **kw) -> AddClientPayload:
    handler = AddClientHandler(uow)
    command = AddClientCommand(**kw)
    result = await handler.execute(command)
    return result.payload


@pytest.fixture
def uow() -> IAuthUnitOfWork:
    """
    Returns auth memory unit of work with cleaned tables
    """

    return memory.AuthInMemoryUnitOfWork(
        clients=memory.ClientInMemoryRepository,
    )
