from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from auth.domain.entities import ClientId
from auth.domain.uow import IAuthUnitOfWork
from shared.application.commands import ICommandHandler, Command, CommandResult


class AddClientCommand(Command):
    username: str


class AddClientResult(CommandResult):
    id: ClientId
    username: str
    date_joined: datetime
    last_login: Optional[datetime] = None


@dataclass(frozen=True, slots=True)
class AddClientHandler(ICommandHandler):
    uow: IAuthUnitOfWork

    async def execute(self, command: AddClientCommand) -> AddClientResult:
        client_dict = command.model_dump()
        async with self.uow:
            client = await self.uow.clients.add(**client_dict)
            result = AddClientResult.model_validate(client)
            await self.uow.commit()
            return result
