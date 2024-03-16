from dataclasses import dataclass
from typing import Optional

from pydantic import ValidationError, BaseModel

from post.domain.entitites import Post
from post.domain.repositories import IPostUnitOfWork
from shared.application.commands import Command, CommandResult
from shared.domain.errors import Error


@dataclass(kw_only=True)
class CreatePostCommand(Command):
    id: Optional[int] = None
    title: str
    content: str
    draft: bool = False


class CreatePostPayload(BaseModel):
    id: int


async def create_post_handler(
    command: CreatePostCommand,
    uow: IPostUnitOfWork,
) -> CommandResult:
    async with uow:
        try:
            post = Post(**command.as_dict(exclude_none=True))
        except ValidationError as e:
            return CommandResult(error=Error.validation(e.errors()))
        
        # try:
        post_id = await uow.posts.add(post)
        # except IdIsAlreadyExistError:
        #     return CommandResult(error=Error.conflict())
        
        await uow.commit()
        return CommandResult(payload={"id": post_id})
