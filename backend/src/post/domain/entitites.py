from dataclasses import dataclass

from shared.domain.entities import AggregateRoot


@dataclass(kw_only=True)
class Post(AggregateRoot):
    title: str
    content: str
    draft: bool = False
