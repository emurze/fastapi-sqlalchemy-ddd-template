from dataclasses import dataclass
from typing import NewType

from shared.domain.events import Event
from shared.domain.value_objects import lazy, metadata
from shared.utils.functional import invisible_field

EntityId = NewType("EntityId", int)


@dataclass(kw_only=True)
class Entity:
    id: lazy[int] = metadata("autoincrement")
    _events: list = invisible_field(default_factory=list)

    def register_event(self, event: Event) -> None:
        self._events.append(event)

    def update(self, **kw) -> None:
        assert kw.get("id") is None, "Entity can't update id"
        for key, value in kw.items():
            setattr(self, key, value)

    def to_dict(self) -> dict:
        return {
            attr: value
            for attr in self.__dataclass_fields__  # noqa
            if (
                not isinstance((value := getattr(self, attr)), metadata)
                and not attr.startswith("_")
            )
        }


class AggregateRoot(Entity):
    """Root Aggregate"""
