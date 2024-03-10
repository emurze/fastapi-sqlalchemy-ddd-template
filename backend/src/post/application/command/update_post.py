from dataclasses import dataclass

from post.application.command import CreatePostCommand
from post.domain.repositories import IPostUnitOfWork
from shared.application.commands import ICommandHandler
from shared.application import dtos
from shared.domain.exceptions import ResourceNotFoundException


class UpdatePostCommand(CreatePostCommand):
    id: int


@dataclass(frozen=True, slots=True)
class UpdatePostHandler(ICommandHandler):
    uow: IPostUnitOfWork

    async def handle(self, command: UpdatePostCommand) -> dtos.OutputDto:
        try:
            command_dict = command.model_dump(exclude={"id"})
            async with self.uow:
                post = await self.uow.posts.get_for_update(id=command.id)
                post.update(**command_dict)
                await self.uow.commit()
                return dtos.SuccessOutputDto()

        except ResourceNotFoundException:
            return dtos.FailedOutputDto.build_resource_not_found_error()

        except SystemError:
            return dtos.FailedOutputDto.build_system_error()
