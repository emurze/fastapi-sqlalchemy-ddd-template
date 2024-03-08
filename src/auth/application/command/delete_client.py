from auth.application import auth_module
from auth.application.command.create_client import CreateClientCommand
from auth.domain.uow import IAuthUnitOfWork
from shared.application.command_handler import ICommandHandler
from shared.application.commands import CommandResult


class DeleteClientCommand(CreateClientCommand):
    id: int


@auth_module.dataclass_command_handler
class DeleteClientHandler(ICommandHandler):
    uow: IAuthUnitOfWork

    async def execute(self, command: DeleteClientCommand) -> CommandResult:
        try:
            async with self.uow:
                await self.uow.clients.delete(id=command.id)
                await self.uow.commit()
                return CommandResult()
        except SystemError:
            return CommandResult.build_system_error()
