import uuid
from pydantic import Field

from seedwork.application.commands import Command
from seedwork.application.dtos import DTO
from spiking.domain.entities import Post
from spiking.domain.events import PostCreatedEvent
from spiking.domain.uows import IUnitOfWork


class AuthorDTO(DTO):
    id: uuid.UUID
    name: str


class CreatePostCommand(Command):
    """
    Syntax validation checks like required fields and permissible ranges.
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    name: str = Field(max_length=64)
    description: str = Field(max_length=256)
    rate: int = Field(ge=1, le=10)
    photo: str | None = None
    draft: bool = True
    authors: list[AuthorDTO] = []


async def create_post(
    command: CreatePostCommand,
    uow: IUnitOfWork,
) -> dict:
    post = Post.model_from(command.model_dump())
    post.add_domain_event(PostCreatedEvent(id=post.id))
    uow.posts.add(post)
    return {"id": command.id}
