from fastapi import Depends

from auth.application.command_handlers.add_client import AddClientHandler
from auth.application.commands import AddClientCommand, UpdateClientCommand
from auth.application.queries import GetClientQuery
from auth.application.query_handlers.get_client import GetClientHandler
from auth.domain.uow import IAuthUnitOfWork as IaUoW
from auth.infra.repositories import in_memory
from shared.application.command_handler import ICommandHandler
from shared.application.commands import CommandResult
from shared.application.queries import QueryResult
from shared.application.query_handler import IQueryHandler


def uow() -> IaUoW:
    return in_memory.AuthInMemoryUnitOfWork(
        clients=in_memory.ClientInMemoryRepository,
    )


class CommandHandlers:
    @staticmethod
    def add_client_handler(_uow: IaUoW = Depends(uow)) -> ICommandHandler:
        return AddClientHandler(_uow)

    async def add_client(self, command: AddClientCommand) -> CommandResult:
        return await self.add_client_handler().execute(command)

    @staticmethod
    def update_client_handler(_uow: IaUoW = Depends(uow)) -> ICommandHandler:
        return AddClientHandler(_uow)

    async def update_client(
         self, command: UpdateClientCommand
    ) -> CommandResult:
        return await self.update_client_handler().execute(command)


class QueryHandlers:
    @staticmethod
    def get_client_handler(_uow: IaUoW = Depends(uow)) -> IQueryHandler:
        return GetClientHandler(_uow)

    async def get_client(self, command: GetClientQuery) -> QueryResult:
        return await self.get_client_handler().execute(command)


command_handlers = CommandHandlers()
query_handlers = QueryHandlers()
