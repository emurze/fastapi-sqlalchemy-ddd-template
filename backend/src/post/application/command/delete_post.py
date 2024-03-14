from post.domain.repositories import IPostUnitOfWork
from shared.application.commands import Command, CommandResult
from shared.domain.entities import EntityId


class DeletePostCommand(Command):
    id: int


async def delete_post_handler(
    command: DeletePostCommand, uow: IPostUnitOfWork
) -> CommandResult:
    try:
        async with uow:
            await uow.posts.delete(entity_id=EntityId(command.id))
            await uow.commit()
            return CommandResult()
    except SystemError:
        return CommandResult.build_system_error()
