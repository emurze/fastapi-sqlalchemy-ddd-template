# import pytest
#
# from auth.application.command.create_client import (
#     CreateClientHandler,
#     CreateClientCommand
# )
# from auth.domain.uow import IAuthUnitOfWork
# from auth.infra.repositories import memory
#
#
# async def make_client(uow: IAuthUnitOfWork, **kw) -> None:
#     handler = CreateClientHandler(uow)
#     command = CreateClientCommand(**kw)
#     await handler.execute(command)
#
#
# @pytest.fixture
# def uow() -> IAuthUnitOfWork:
#     """
#     Returns auth memory unit of work with cleaned tables
#     """
#
#     return memory.AuthInMemoryUnitOfWork(
#         clients=memory.ClientInMemoryRepository,
#     )


def test_pass():
    pass
