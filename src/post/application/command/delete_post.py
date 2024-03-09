from dataclasses import dataclass

from shared.application.command_handler import ICommandHandler
from shared.application.commands import CommandResult, Command
from shared.domain.uow import IGenericUnitOfWork


class DeletePostCommand(Command):
    id: int


@dataclass(frozen=True, slots=True)
class DeletePostHandler(ICommandHandler):
    uow: IGenericUnitOfWork

    async def execute(self, command: DeletePostCommand) -> CommandResult:
        try:
            async with self.uow:
                await self.uow.posts.delete(id=command.id)
                await self.uow.commit()
                return CommandResult()
        except SystemError:
            return CommandResult.build_system_error()
