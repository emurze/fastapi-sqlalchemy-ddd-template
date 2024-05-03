from dataclasses import field, dataclass
from typing import Optional, Any, Self
from uuid import UUID

from dacite import from_dict

from seedwork.domain.events import DomainEvent
from seedwork.domain.services import uuid_field, hidden_field


@dataclass(kw_only=True)
class Entity:
    id: UUID = uuid_field()
    awaitable_attrs: Optional["AwaitableAttrs"] = hidden_field(default=None)

    def __post_init__(self) -> None:
        if not self.awaitable_attrs:
            self.awaitable_attrs = AwaitableAttrs(entity=self)

    @classmethod
    def create(cls, **kw) -> tuple[Self, list[Any]]:
        # validate
        return from_dict(data_class=cls, data=kw), []

    def update(self, **kw) -> Any:  # todo: Error | None
        assert kw.get("id") is None, "Entity can't update its identity."
        for key, value in kw.items():
            setattr(self, key, value)


@dataclass(kw_only=True)
class LocalEntity(Entity):
    """Entity inside an aggregate."""


@dataclass(kw_only=True)
class AggregateRoot(Entity):
    # https://docs.sqlalchemy.org/en/14/orm/composites.html
    # https://blog.szymonmiks.pl/p/what-are-architectural-drivers-in-software-engineering/
    """Consists of 1+ entities. Spans transaction boundaries."""
    events: list[DomainEvent] = field(default_factory=list)

    def add_domain_event(self, event: DomainEvent) -> None:
        self.events.append(event)

    def collect_events(self) -> list[DomainEvent]:
        events = self.events
        self.events = []
        return events


class AwaitableAttrs:
    def __init__(
        self,
        entity: Optional[Entity] = None,
        awaitable_attrs: Optional[Any] = None,
    ) -> None:
        assert entity or awaitable_attrs, (
            "Either entity or awaitable_attrs must be provided."
        )
        assert not (entity and awaitable_attrs), (
            "Only one of entity or awaitable_attrs should be provided."
        )
        self._entity = entity
        self._awaitable_attrs = awaitable_attrs

        def attrs_getter(key: str) -> Any:
            return getattr(self._awaitable_attrs, key)

        async def entity_getter(key: str):
            return getattr(self._entity, key)

        self._getter = attrs_getter if self._awaitable_attrs else entity_getter

    def __getattr__(self, key: str) -> Any:
        if key.startswith("_"):
            return object.__getattribute__(self, key)
        else:
            return self._getter(key)
