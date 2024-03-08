from auth.application import auth_module
from auth.domain.uow import IAuthUnitOfWork
from shared.application.command_handler import ICommandHandler
from shared.application.commands import CommandResult, Command


class CreateClientCommand(Command):
    username: str


@auth_module.dataclass_command_handler
class CreateClientHandler(ICommandHandler):
    uow: IAuthUnitOfWork

    async def execute(self, command: CreateClientCommand) -> CommandResult:
        try:
            client_dict = command.model_dump()
            async with self.uow:
                await self.uow.clients.create(**client_dict)
                await self.uow.commit()
                return CommandResult()
        except SystemError:
            return CommandResult.build_system_error()