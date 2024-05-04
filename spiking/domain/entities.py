import uuid
from dataclasses import dataclass

from seedwork.domain.entities import AggregateRoot, LocalEntity
from spiking.domain.events import PostPublishedEvent, PostPopulatedEvent


@dataclass(kw_only=True)
class Post(AggregateRoot):
    id: uuid.UUID
    name: str
    description: str
    rate: int
    photo: str | None
    draft: bool
    authors: list['Author']

    def publish(self) -> None:
        self.draft = False
        self.add_domain_event(PostPublishedEvent(id=self.id))

    def populate(self) -> None:
        self.rate = 10
        self.add_domain_event(PostPopulatedEvent(id=self.id))

    async def get_first_author(self) -> 'Author':
        return (await self.awaitable_attrs.authors)[0]

    async def update_first_author(self, name: str) -> None:
        author = await self.get_first_author()
        author.name = name


@dataclass(kw_only=True)
class Author(LocalEntity):
    id: uuid.UUID
    name: str
