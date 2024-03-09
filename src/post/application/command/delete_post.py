from dataclasses import dataclass

from shared.application.commands import ICommandHandler, Command
from shared.application.dtos import Result, SuccessResult, FailedResult
from shared.domain.uow import IGenericUnitOfWork


class DeletePostCommand(Command):
    id: int


@dataclass(frozen=True, slots=True)
class DeletePostHandler(ICommandHandler):
    uow: IGenericUnitOfWork

    async def handle(self, command: DeletePostCommand) -> Result:
        try:
            async with self.uow:
                await self.uow.posts.delete(id=command.id)
                await self.uow.commit()
                return SuccessResult()
        except SystemError:
            return FailedResult.build_system_error()
