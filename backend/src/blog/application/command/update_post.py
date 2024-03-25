from dataclasses import dataclass

from pydantic import ValidationError

from seedwork.application.commands import Command, CommandResult
from shared_kernel.domain.errors import Error
from seedwork.domain.uows import IUnitOfWork


@dataclass(kw_only=True)
class UpdatePostCommand(Command):
    id: int
    title: str
    content: str
    draft: bool = False


async def update_post_handler(
    command: UpdatePostCommand,
    uow: IUnitOfWork,
) -> CommandResult:
    async with uow:
        post = await uow.posts.get_by_id(command.id, for_update=True)

        if post is None:
            return CommandResult(error=Error.not_found())

        try:
            post.update(**command.as_dict(exclude={"id"}))
        except ValidationError as e:
            return CommandResult(error=Error.validation(e.errors()))

        await uow.commit()
        return CommandResult()
