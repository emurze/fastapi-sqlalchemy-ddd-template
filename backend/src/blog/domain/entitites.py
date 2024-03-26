from pydantic import Field

from blog.domain.events import PostAlreadyExist
from seedwork.domain.entities import AggregateRoot, LocalEntity


class Publisher(LocalEntity):
    name: str = Field(max_length=128)
    # posts: list['Post'] = []


class Post(AggregateRoot):
    title: str = Field(max_length=256)
    content: str = Field(max_length=256)
    draft: bool = False
    # publisher: Publisher

    def publish(self) -> None:
        self.register_event(PostAlreadyExist("VLADOS"))

