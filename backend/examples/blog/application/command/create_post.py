from dataclasses import dataclass
from typing import Optional

from pydantic import ValidationError

from blog.domain.entitites import Post, Author
from seedwork.application.commands import Command, CommandResult
from seedwork.application.dtos import DTO
from seedwork.domain.errors import Error, EntityAlreadyExistsError
from seedwork.domain.uows import IUnitOfWork


@dataclass(kw_only=True)
class CreatePostCommand(Command):
    id: Optional[int] = None
    title: str
    content: str
    draft: bool = False
    author_id: int
    account_id: int


@dataclass(kw_only=True)
class CreatePostPayload(DTO):
    id: int


async def create_post_handler(
    command: CreatePostCommand,
    uow: IUnitOfWork,
) -> CommandResult:
    async with uow:
        _dict = command.as_dict(exclude={"author_id"})
        _dict["author"] = Author(
            id=command.author_id,
            account_id=command.account_id
        )
        try:
            post = Post(**_dict)
        except ValidationError as e:
            return CommandResult(error=Error.validation(e.errors()))

        try:
            post_id = await uow.posts.add(post)
        except EntityAlreadyExistsError:
            return CommandResult(error=Error.conflict())

        await uow.commit()
        return CommandResult(payload=CreatePostPayload(id=post_id))
