from dataclasses import dataclass
from typing import Optional, Union

from post.domain.entitites import Post
from post.domain.repositories import IPostUnitOfWork
from shared.application.commands import ICommandHandler, Command
from shared.application.dtos import SuccessOutputDto, FailedOutputDto

CreatePostOrFail = Union["CreatePostOutputDto", FailedOutputDto]


class CreatePostCommand(Command):
    id: Optional[int] = None
    title: str
    content: str
    draft: bool = False


class CreatePostOutputDto(SuccessOutputDto):
    id: int


@dataclass(frozen=True, slots=True)
class CreatePostHandler(ICommandHandler):
    uow: IPostUnitOfWork

    async def handle(self, command: CreatePostCommand) -> CreatePostOrFail:
        try:
            async with self.uow:
                post = Post(title="Post 1", content="Content 1")
                post_id = await self.uow.posts.add(post)
                await self.uow.commit()
                return CreatePostOutputDto(id=post_id)
        except SystemError:
            return FailedOutputDto.build_system_error()
