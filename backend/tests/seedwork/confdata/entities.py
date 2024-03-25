from pydantic import Field

from seedwork.domain.entities import AggregateRoot


class Example(AggregateRoot):
    name: str = Field(max_length=10)
