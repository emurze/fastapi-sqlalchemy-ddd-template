from collections.abc import Callable
from typing import Any, cast
from uuid import UUID

from pydantic import ConfigDict, BaseModel
from pydantic.fields import PrivateAttr

from seedwork.domain.events import DomainEvent
from seedwork.domain.services import UUIDField
from seedwork.utils.functional import classproperty, get_single_param


class FieldWrapper:
    def __init__(self, field: Any, entity: type[BaseModel]) -> None:
        self._entity = entity
        self._field = field

    def __getattr__(self, constraint_name: str) -> Any:
        for item in self._field.metadata:
            return getattr(item, constraint_name)


class EntityWrapper:
    def __init__(self, entity: type[BaseModel]) -> None:
        self._entity = entity

    def __getattr__(self, field_name: str) -> Any:
        field_info = self._entity.model_fields[field_name]
        return FieldWrapper(field_info, self._entity)


class Entity(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )
    id: UUID = UUIDField
    _extra: dict = PrivateAttr(default_factory=lambda: {"actions": []})

    def __setattr__(self, key, value) -> None:
        self.extra["actions"].append((key, value))
        super().__setattr__(key, value)

    @property
    def extra(self) -> dict:
        return self._extra

    @classproperty
    def c(self) -> EntityWrapper:
        cls = cast(type[BaseModel], self)
        return EntityWrapper(cls)

    def update(self, **kw) -> None:
        assert kw.get("id") is None, "Entity can't update its identity."
        for key, value in kw.items():
            setattr(self, key, value)

    def persist(self, mapper: Callable) -> dict:
        entity_relation = getattr(self, rel_name := get_single_param(mapper))

        if not entity_relation.__load_entity_list().__is_loaded():
            return {}

        if entity_relation.__is_entity_list():
            return {rel_name: mapper(entity_relation)}
        else:
            entity_relation.__execute_actions(mapper)
            mapper(entity_relation)
            return {}


class LocalEntity(Entity):
    """Entity inside an aggregate."""


class AggregateRoot(Entity):
    """Consists of 1+ entities. Spans transaction boundaries."""

    _events: list[DomainEvent] = []

    def add_domain_event(self, event: DomainEvent) -> None:
        self._events.append(event)

    def collect_events(self) -> list[DomainEvent]:
        events = self._events
        self._events = []
        return events
