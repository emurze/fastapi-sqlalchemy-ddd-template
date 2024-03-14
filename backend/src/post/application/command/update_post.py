from post.domain.repositories import IPostUnitOfWork
from shared.application.commands import CommandResult, Command
from shared.domain.exceptions import ResourceNotFoundException


class UpdatePostCommand(Command):
    id: int
    title: str
    content: str
    draft: bool = False


async def update_post_handler(
    command: UpdatePostCommand, uow: IPostUnitOfWork
) -> CommandResult:
    try:
        command_dict = command.model_dump(exclude={"id"})
        async with uow:
            post = await uow.posts.get_for_update(id=command.id)
            post.update(**command_dict)
            await uow.commit()
            return CommandResult()

    except ResourceNotFoundException:
        return CommandResult.build_resource_not_found_error()

    except SystemError:
        return CommandResult.build_system_error()
