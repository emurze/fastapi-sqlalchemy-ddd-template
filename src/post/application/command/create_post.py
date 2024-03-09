from dataclasses import dataclass
from typing import Optional

from shared.application.command_handler import ICommandHandler
from shared.application.commands import CommandResult, Command, CommandPayload
from shared.domain.uow import IGenericUnitOfWork


class CreatePostCommand(Command):
    id: Optional[int] = None
    title: str
    content: str
    draft: bool


class CreatePostPayload(CommandPayload):
    id: int


@dataclass(frozen=True, slots=True)
class CreatePostHandler(ICommandHandler):
    uow: IGenericUnitOfWork

    async def execute(self, command: CreatePostCommand) -> CommandResult:
        try:
            client_dict = command.model_dump(exclude_none=True)
            async with self.uow:
                client_id = await self.uow.posts.create(**client_dict)
                payload = CreatePostPayload(id=client_id)
                await self.uow.commit()
                return CommandResult(payload=payload)
        except SystemError:
            return CommandResult.build_system_error()
