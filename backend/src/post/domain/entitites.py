from pydantic import Field
from pydantic.v1.dataclasses import dataclass

from shared.domain.entities import AggregateRoot


@dataclass(kw_only=True)
class Post(AggregateRoot):
    title: str = Field(max_length=256)
    content: str = Field(max_length=256)
    draft: bool = False
