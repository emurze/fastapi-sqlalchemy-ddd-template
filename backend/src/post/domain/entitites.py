from shared.domain.entities import AggregateRoot
from shared.domain.pydantic_v1 import py_dataclass, Field


@py_dataclass(kw_only=True)
class Post(AggregateRoot):
    title: str = Field(max_length=256)
    content: str = Field(max_length=256)
    draft: bool = False
