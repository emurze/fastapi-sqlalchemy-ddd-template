from dataclasses import dataclass

from auth.application.commands.delete_client import (
    DeleteClientCommand,
    DeleteClientPayload,
    DeleteClientResult,
)
from auth.domain.uow import IAuthUnitOfWork
from shared.application.command_handler import ICommandHandler
from shared.domain.exceptions import ResourceNotFoundError


@dataclass(frozen=True, slots=True)
class DeleteClientHandler(ICommandHandler):
    uow: IAuthUnitOfWork

    async def execute(
        self, command: DeleteClientCommand,
    ) -> DeleteClientResult:
        try:
            cmd_dict = command.model_dump()
            async with self.uow:
                deleted_client = await self.uow.clients.delete_one(**cmd_dict)
                payload = DeleteClientPayload.model_validate(deleted_client)
                return DeleteClientResult(payload=payload)
        except ResourceNotFoundError:
            return DeleteClientResult.build_resource_not_found_error()
        except SystemError:
            return DeleteClientResult.build_system_error()
