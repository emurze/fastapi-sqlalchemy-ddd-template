from dataclasses import dataclass

from post.domain.repositories import IPostUnitOfWork
from shared.application.commands import ICommandHandler, Command
from shared.application import dtos
from shared.domain.entities import EntityId


class DeletePostCommand(Command):
    id: int


@dataclass(frozen=True, slots=True)
class DeletePostHandler(ICommandHandler):
    uow: IPostUnitOfWork

    async def handle(self, command: DeletePostCommand) -> dtos.OutputDto:
        try:
            async with self.uow:
                await self.uow.posts.delete(entity_id=EntityId(command.id))
                await self.uow.commit()
                return dtos.SuccessOutputDto()
        except SystemError:
            return dtos.FailedOutputDto.build_system_error()
