from auth.application.command_handlers.update_client import UpdateClientHandler
from auth.application.commands.update_client import UpdateClientCommand
from auth.domain.uow import IAuthUnitOfWork
from tests.auth.application.conftest import make_client


async def test_can_update_client(uow: IAuthUnitOfWork) -> None:
    await make_client(uow, username="Vlad")

    handler = UpdateClientHandler(uow)
    command = UpdateClientCommand(id=1, username="New Vlad")
    result = await handler.execute(command)
    client = result.payload

    assert client.id == 1
    assert client.username == "New Vlad"


async def test_can_create_client(uow: IAuthUnitOfWork) -> None:
    handler = UpdateClientHandler(uow)
    command = UpdateClientCommand(id=1, username="New Vlad")
    result = await handler.execute(command)
    client = result.payload

    assert client.id == 1
    assert client.username == "New Vlad"
