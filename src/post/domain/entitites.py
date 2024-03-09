from dataclasses import dataclass

from shared.domain.entities import AggregateRoot


@dataclass
class Post(AggregateRoot):
    id: int
    title: str
    content: str
    draft: bool = False
