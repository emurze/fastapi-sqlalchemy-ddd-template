from dataclasses import dataclass

from post.domain.repositories import IPostUnitOfWork
from shared.application.commands import Command, CommandResult
from shared.domain.errors import Error


@dataclass(kw_only=True)
class UpdatePostCommand(Command):
    id: int
    title: str
    content: str
    draft: bool = False


async def update_post_handler(
    command: UpdatePostCommand,
    uow: IPostUnitOfWork,
) -> CommandResult:
    async with uow:
        post = await uow.posts.get_by_id(command.id, for_update=True)

        if post is None:
            return CommandResult(error=Error.not_found())

        post.update(**command.as_dict(exclude={"id"}))
        await uow.commit()
        return CommandResult()
