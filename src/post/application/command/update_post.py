from dataclasses import dataclass

from post.application.command import CreatePostCommand
from shared.application.command_handler import ICommandHandler
from shared.application.commands import CommandResult
from shared.domain.exceptions import ResourceNotFoundError
from shared.domain.uow import IGenericUnitOfWork


class UpdatePostCommand(CreatePostCommand):
    id: int


@dataclass(frozen=True, slots=True)
class UpdatePostHandler(ICommandHandler):
    uow: IGenericUnitOfWork

    async def execute(self, command: UpdatePostCommand) -> CommandResult:
        try:
            command_dict = command.model_dump(exclude=["id"])
            async with self.uow:
                post = await self.uow.posts.get_for_update(id=command.id)
                post.update(**command_dict)
                await self.uow.commit()
                return CommandResult()

        except ResourceNotFoundError:
            return CommandResult.build_resource_not_found_error()

        except SystemError:
            return CommandResult.build_system_error()
