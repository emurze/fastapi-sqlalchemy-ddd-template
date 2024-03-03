from dataclasses import dataclass, field
from typing import TypeVar, Generic

EntityId = TypeVar('EntityId')


@dataclass
class Entity(Generic[EntityId]):
    id: EntityId = field(hash=True)

    def update(self, **kw) -> None:
        assert kw.get('id') is None, "Entity can't update id"
        for key, value in kw.items():
            setattr(self, key, value)


class AggregateRoot(Entity[EntityId]):
    """Root Aggregate"""
