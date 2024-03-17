import logging
from dataclasses import dataclass
from typing import Optional

from post.domain.entitites import Post
from post.domain.repositories import IPostUnitOfWork
from shared.application.commands import Command, CommandResult
from shared.application.dtos import DTO
from shared.domain.errors import Error
from shared.domain.pydantic_v1 import ValidationError

lg = logging.getLogger(__name__)


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
    uow: IPostUnitOfWork,
) -> CommandResult:
    lg.debug('Running create_post_handler')
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
        return CommandResult(payload=CreatePostPayload(id=post_id))
