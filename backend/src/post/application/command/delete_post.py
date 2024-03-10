from dataclasses import dataclass

from post.domain.repositories import IPostUnitOfWork
from shared.application.commands import ICommandHandler, Command
from shared.application import dtos


class DeletePostCommand(Command):
    id: int


@dataclass(frozen=True, slots=True)
class DeletePostHandler(ICommandHandler):
    uow: IPostUnitOfWork

    async def handle(self, command: DeletePostCommand) -> dtos.OutputDto:
        try:
            async with self.uow:
                await self.uow.posts.delete(id=command.id)
                await self.uow.commit()
                return dtos.SuccessOutputDto()
        except SystemError:
            return dtos.FailedOutputDto.build_system_error()
