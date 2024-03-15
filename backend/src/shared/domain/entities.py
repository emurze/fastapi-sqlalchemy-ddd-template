from dataclasses import dataclass

from shared.domain.events import Event
from shared.domain.value_objects import lazy, metadata
from shared.utils.functional import invisible_field


@dataclass(kw_only=True)
class Entity:
    id: lazy[int] = metadata("autoincrement")

    def __hash__(self) -> int:
        assert self.id != metadata  # check it
        return hash(self.id)

    def update(self, **kw) -> None:
        assert kw.get("id") is None, "Entity can't update id"
        for key, value in kw.items():
            setattr(self, key, value)

    def as_dict(self) -> dict:
        return {
            attr: value
            for attr in self.__dataclass_fields__  # noqa
            if (
                not isinstance((value := getattr(self, attr)), metadata)
                and not attr.startswith("_")
            )
        }


@dataclass(kw_only=True)
class AggregateRoot(Entity):
    """Consists of 1+ entities. Spans transaction boundaries."""

    events: list = invisible_field(default_factory=list)

    def register_event(self, event: Event) -> None:
        self.events.append(event)

    def collect_events(self):
        pass
