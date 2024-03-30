from dataclasses import dataclass


from seedwork.application.commands import Command, CommandResult
from seedwork.domain.uows import IUnitOfWork


@dataclass(kw_only=True)
class DeletePostCommand(Command):
    id: int


async def delete_post_handler(
    command: DeletePostCommand,
    uow: IUnitOfWork,
) -> CommandResult:
    async with uow:
        await uow.posts.delete_by_id(command.id)
        await uow.commit()
        return CommandResult()
