from dataclasses import dataclass

from auth.application.commands.delete_client import (
    DeleteClientCommand,
    DeleteClientPayload,
    DeleteClientResult,
)
from auth.domain.uow import IAuthUnitOfWork
from shared.application.command_handler import ICommandHandler


@dataclass(frozen=True, slots=True)
class DeleteClientHandler(ICommandHandler):
    uow: IAuthUnitOfWork

    async def execute(
        self, command: DeleteClientCommand,
    ) -> DeleteClientResult:
        command_dict = command.model_dump()
        async with self.uow:
            deleted_client = await self.uow.clients.delete_one(**command_dict)
            payload = DeleteClientPayload.model_validate(deleted_client)
            return DeleteClientResult(payload=payload)
