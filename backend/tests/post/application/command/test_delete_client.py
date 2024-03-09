# import pytest
#
# from auth.application.command.delete_client import (
#     DeleteClientCommand,
#     DeleteClientCommandHandler,
# )
# from auth.domain import IAuthUnitOfWork
# from tests.auth.application.conftest import make_client
#
#
# @pytest.mark.unit
# async def test_can_delete_client(uow: IAuthUnitOfWork) -> None:
#     await make_client(uow, username="Vlad")
#
#     handler = DeleteClientCommandHandler(uow)
#     command = DeleteClientCommand(id=1)
#     await handler.execute(command)
#     #
# assert result.status is True
# assert deleted_client.id == 1
# assert deleted_client.username == "Vlad"

#
# @pytest.mark.unit
# async def test_delete_client_not_found_error(uow: IAuthUnitOfWork) -> None:
#     # handler = DeleteClientHandler(uow)
#     # command = DeleteClientCommand(id=1)
#     # result = await handler.execute(command)
#     # assert result.status is False
#     pass
