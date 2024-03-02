from dataclasses import dataclass, field
from typing import TypeVar, Generic

EntityId = TypeVar('EntityId')


@dataclass
class Entity(Generic[EntityId]):
    id: EntityId = field(hash=True)


class AggregateRoot(Entity[EntityId]):
    """Root Aggregate"""
