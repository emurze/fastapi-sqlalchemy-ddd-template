from dataclasses import dataclass
from typing import Optional, Union

from post.domain.repositories import IPostUnitOfWork
from shared.application.commands import ICommandHandler, Command

from shared.application.dtos import SuccessResult, FailedResult

CreatePostOrFail = Union['CreatePostResult', FailedResult]


class CreatePostCommand(Command):
    id: Optional[int] = None
    title: str
    content: str
    draft: bool


class CreatePostResult(SuccessResult):
    id: int


@dataclass(frozen=True, slots=True)
class CreatePostHandler(ICommandHandler):
    uow: IPostUnitOfWork

    async def handle(self, command: CreatePostCommand) -> CreatePostOrFail:
        try:
            client_dict = command.model_dump(exclude_none=True)
            async with self.uow:
                client_id = await self.uow.posts.create(**client_dict)
                await self.uow.commit()
                return CreatePostResult(id=client_id)
        except SystemError:
            return FailedResult.build_system_error()
