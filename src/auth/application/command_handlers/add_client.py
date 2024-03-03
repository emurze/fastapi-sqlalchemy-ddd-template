from dataclasses import dataclass

from auth.application.commands.add_client import (
    AddClientCommand,
    AddClientResult,
    AddClientPayload,
)
from auth.domain.uow import IAuthUnitOfWork
from shared.application.command_handler import ICommandHandler


@dataclass(frozen=True, slots=True)
class AddClientHandler(ICommandHandler):
    uow: IAuthUnitOfWork

    async def execute(self, command: AddClientCommand) -> AddClientResult:
        client_dict = command.model_dump()
        async with self.uow:
            client = await self.uow.clients.add(**client_dict)
            payload = AddClientPayload.model_validate(client)
            await self.uow.commit()
            return AddClientResult(payload=payload)
