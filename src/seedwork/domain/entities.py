import dacite

from dataclasses import dataclass
from typing import Optional, Any, Self
from uuid import UUID

from seedwork.domain.events import DomainEvent
from seedwork.domain.mixins import BusinessRuleValidationMixin
from seedwork.domain.services import uuid_field


@dataclass(kw_only=True)
class Entity:
    id: UUID = uuid_field()

    def __post_init__(self) -> None:
        if not hasattr(self, "_awaitable_attrs"):
            self._awaitable_attrs = AwaitableAttrs(entity=self)

    @property
    def awaitable_attrs(self) -> 'AwaitableAttrs':
        return self._awaitable_attrs

    @classmethod
    def model_from(cls, data: dict) -> Self:
        return dacite.from_dict(data_class=cls, data=data)

    def update(self, **kw) -> Any:
        assert kw.get("id") is None, "Entity can't update its identity."
        for key, value in kw.items():
            setattr(self, key, value)


@dataclass(kw_only=True)
class LocalEntity(Entity):
    """Entity inside an aggregate."""


@dataclass(kw_only=True)
class AggregateRoot(BusinessRuleValidationMixin, Entity):
    # https://docs.sqlalchemy.org/en/14/orm/composites.html
    # https://blog.szymonmiks.pl/p/what-are-architectural-drivers-in-software-engineering/
    """Consists of 1+ entities. Spans transaction boundaries."""
    def __post_init__(self) -> None:
        self._events: list[DomainEvent] = []

    def add_domain_event(self, event: DomainEvent) -> None:
        self._events.append(event)

    def collect_events(self) -> list[DomainEvent]:
        events = self._events
        self._events = []
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
