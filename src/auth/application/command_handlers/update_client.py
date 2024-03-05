from dataclasses import dataclass

from auth.application.commands.update_client import (
    UpdateClientCommand,
    UpdateClientPayload,
    UpdateClientResult,
)
from auth.domain.uow import IAuthUnitOfWork
from shared.application.command_handler import ICommandHandler
from shared.domain.exceptions import ResourceNotFoundError


@dataclass(frozen=True, slots=True)
class UpdateClientHandler(ICommandHandler):
    uow: IAuthUnitOfWork

    async def execute(
        self, command: UpdateClientCommand,
    ) -> UpdateClientResult:
        try:
            command_dict = command.model_dump(exclude=["id"])
            async with self.uow:
                try:
                    client = await self.uow.clients.get_for_update(
                        id=command.id
                    )
                    client.update(**command_dict)

                except ResourceNotFoundError:
                    client = await self.uow.clients.add(**command_dict)

                payload = UpdateClientPayload.model_validate(client)
                await self.uow.commit()
                return UpdateClientResult(payload=payload)
        except SystemError:
            return UpdateClientResult.build_system_error()
