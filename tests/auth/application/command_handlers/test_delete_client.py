from auth.application.command_handlers.delete_client import DeleteClientHandler
from auth.application.commands.delete_client import DeleteClientCommand
from auth.domain.uow import IAuthUnitOfWork
from tests.auth.application.conftest import make_client


async def test_can_delete_client(uow: IAuthUnitOfWork) -> None:
    await make_client(uow, username="Vlad")

    handler = DeleteClientHandler(uow)
    command = DeleteClientCommand(id=1)
    result = await handler.execute(command)
    deleted_client = result.payload

    assert result.status is True
    assert deleted_client.id == 1
    assert deleted_client.username == "Vlad"


async def test_delete_client_not_found_error(uow: IAuthUnitOfWork) -> None:
    handler = DeleteClientHandler(uow)
    command = DeleteClientCommand(id=1)
    result = await handler.execute(command)
    assert result.status is False
