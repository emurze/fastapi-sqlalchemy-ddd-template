from dataclasses import dataclass

from auth.application.commands.update_client import (
    UpdateClientCommand,
    UpdateClientPayload,
    UpdateClientResult,
)
from auth.domain.uow import IAuthUnitOfWork
from shared.application.command_handler import ICommandHandler


@dataclass(frozen=True, slots=True)
class UpdateClientHandler(ICommandHandler):
    uow: IAuthUnitOfWork

    async def execute(
        self, command: UpdateClientCommand,
    ) -> UpdateClientResult:
        command_dict = command.model_dump(exclude=["id"])
        async with self.uow:
            client = await self.uow.clients.get(id=command.id)
            client.update(**command_dict)
            payload = UpdateClientPayload.model_validate(client)
            await self.uow.commit()
            return UpdateClientResult(payload=payload)
