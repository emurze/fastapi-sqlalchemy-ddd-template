from dataclasses import dataclass
from typing import Optional

from pydantic import ValidationError

from blog.domain.entitites import Post
from blog.domain.events import PostAlreadyExist
from seedwork.application.commands import Command, CommandResult
from seedwork.application.dtos import DTO
from seedwork.domain.errors import Error, EntityAlreadyExistsError
from seedwork.domain.uows import IUnitOfWork


@dataclass(kw_only=True)
class CreatePostCommand(Command):
    id: Optional[int] = 1
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
            post = Post(**command.as_dict(exclude_none=True))
        except ValidationError as e:
            return CommandResult(error=Error.validation(e.errors()))

        post.publish()

        try:
            post_id = await uow.posts.add(post)
        except EntityAlreadyExistsError:
            return CommandResult(
                error=Error.conflict(),
                events=[PostAlreadyExist(message="LERKA")],
            )

        await uow.commit()
        return CommandResult(payload=CreatePostPayload(id=post_id))
