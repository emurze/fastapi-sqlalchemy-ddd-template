from dataclasses import dataclass
from typing import Optional

from post.domain.entitites import Post
from post.domain.repositories import IPostUnitOfWork
from shared.application.commands import Command, CommandResult
from shared.utils.functional import as_model


@dataclass(kw_only=True)
class CreatePostCommand(Command):
    id: Optional[int] = None
    title: str
    content: str
    draft: bool = False


async def create_post_handler(
    command: CreatePostCommand, uow: IPostUnitOfWork
) -> CommandResult:
    async with uow:
        post = Post(**command.as_dict())
        post_id = await uow.posts.add(post)
        await uow.commit()
        return CommandResult(payload=as_model({"id": post_id}))
