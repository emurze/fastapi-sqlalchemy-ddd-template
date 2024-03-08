from auth.application import auth_module
from auth.application.command.create_client import CreateClientCommand
from auth.domain.uow import IAuthUnitOfWork
from shared.application.command_handler import ICommandHandler
from shared.application.commands import CommandResult
from shared.domain.exceptions import ResourceNotFoundError


class UpdateClientCommand(CreateClientCommand):
    id: int


@auth_module.dataclass_command_handler
class UpdateClientCommandHandler(ICommandHandler):
    uow: IAuthUnitOfWork

    async def execute(self, command: UpdateClientCommand) -> CommandResult:
        try:
            command_dict = command.model_dump(exclude=["id"])
            async with self.uow:
                try:
                    client = await self.uow.clients.get_for_update(
                        id=command.id
                    )
                    client.update(**command_dict)

                except ResourceNotFoundError:
                    await self.uow.clients.create(**command_dict)

                await self.uow.commit()
                return CommandResult()
        except SystemError:
            return CommandResult.build_system_error()
