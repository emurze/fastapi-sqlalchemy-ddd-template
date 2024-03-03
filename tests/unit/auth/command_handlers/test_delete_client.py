from auth.application.command_handlers.delete_client import DeleteClientHandler
from auth.application.commands.delete_client import DeleteClientCommand
from auth.domain.uow import IAuthUnitOfWork
from tests.unit.auth.conftest import make_client


async def test_delete_client_handler(uow: IAuthUnitOfWork) -> None:
    await make_client(uow, username="Vlad")

    handler = DeleteClientHandler(uow)
    command = DeleteClientCommand(id=1)
    result = await handler.execute(command)
    deleted_client = result.payload

    assert deleted_client.id == 1
    assert deleted_client.username == "Vlad"
