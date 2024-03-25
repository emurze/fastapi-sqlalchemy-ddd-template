from dataclasses import dataclass
from typing import Optional

from pydantic import ValidationError

from blog.domain.entitites import Post
from seedwork.application.commands import Command, CommandResult
from seedwork.application.dtos import DTO
from shared_kernel.domain.errors import Error, EntityAlreadyExistsError

from seedwork.domain.uows import IUnitOfWork


@dataclass(kw_only=True)
class CreatePostCommand(Command):
    id: Optional[int] = None
    title: str
    content: str
    draft: bool = False


@dataclass(kw_only=True)
class CreatePostPayload(DTO):
    id: int


async def create_post_handler(
    command: CreatePostCommand,
    uow: IUnitOfWork,
) -> CommandResult:
    async with uow:
        try:
            post = Post(**(command.as_dict(exclude_none=True)))
        except ValidationError as e:
            return CommandResult(error=Error.validation(e.errors()))

        try:
            post_id = await uow.posts.add(post)
        except EntityAlreadyExistsError:
            return CommandResult(error=Error.conflict())

        await uow.commit()
        return CommandResult(payload=CreatePostPayload(id=post_id))
