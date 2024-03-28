from typing import Iterator, Any

from pydantic import ConfigDict, BaseModel

from seedwork.domain.events import Event
from seedwork.domain.value_objects import Deferred, deferred


class Entity(BaseModel):
    model_config = ConfigDict(validate_assignment=True, from_attributes=True)
    id: deferred[int] = Deferred

    def _get_deferred_fields(self) -> Iterator[str]:
        for key in self.model_fields.keys():
            if getattr(self, key) == Deferred:
                yield key

    def insert_deferred_values(self, model: Any) -> None:
        for field in self._get_deferred_fields():
            setattr(self, field, getattr(model, field))

    def model_dump(self, *args, exclude_deferred: bool = False, **kw) -> dict:
        if exclude_deferred:
            deferred_fields = set(self._get_deferred_fields())
            kw["exclude"] = kw.get("exclude", set()) | deferred_fields
        return super().model_dump(*args, **kw)

    def update(self, **kw) -> None:
        assert kw.get("id") is None, "Entity can't update its identity."
        for key, value in kw.items():
            setattr(self, key, value)

    def __str__(self) -> str:
        default_str = super().__str__()
        return f"{type(self).__name__}({', '.join(default_str.split())})"


class LocalEntity(Entity):
    """Entity inside an aggregate."""


class AggregateRoot(Entity):
    """Consists of 1+ entities. Spans transaction boundaries."""

    _events: list[Event] = []

    def register_event(self, event: Event) -> None:
        self._events.append(event)

    def collect_events(self) -> list[Event]:
        events = self._events
        self._events = []
        return events
