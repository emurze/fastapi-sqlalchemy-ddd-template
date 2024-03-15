from dataclasses import dataclass

from post.domain.repositories import IPostUnitOfWork
from shared.application.commands import Command, CommandResult


@dataclass(kw_only=True)
class DeletePostCommand(Command):
    id: int


async def delete_post_handler(
    command: DeletePostCommand,
    uow: IPostUnitOfWork,
) -> CommandResult:
    async with uow:
        await uow.posts.delete_by_id(command.id)
        await uow.commit()
        return CommandResult()
