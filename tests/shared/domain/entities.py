from dataclasses import dataclass

from shared.domain.entities import AggregateRoot


@dataclass(kw_only=True)
class Example(AggregateRoot):
    name: str
