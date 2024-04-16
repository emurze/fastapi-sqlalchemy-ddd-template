import inspect
from collections.abc import Callable
from typing import Any, cast
from uuid import UUID

from pydantic import ConfigDict, BaseModel
from pydantic.fields import FieldInfo, PrivateAttr

from seedwork.domain.events import Event
from seedwork.domain.services import UUIDField
from seedwork.utils.functional import classproperty


class FieldWrapper:
    def __init__(self, field: FieldInfo, entity: type[BaseModel]) -> None:
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
    _extra: dict = PrivateAttr(default_factory=dict)

    @property
    def extra_kw(self) -> dict:
        return self._extra

    @classproperty
    def c(self) -> EntityWrapper:
        cls = cast(type[BaseModel], self)
        return EntityWrapper(cls)

    def update(self, **kw) -> None:
        assert kw.get("id") is None, "Entity can't update its identity."
        for key, value in kw.items():
            setattr(self, key, value)

    @staticmethod
    def _get_mapper_param(mapper: Callable) -> str:
        res = inspect.signature(mapper)
        params = tuple(res.parameters)
        assert len(params) == 1, "Map callback should have only one parameter."
        return params[0]

    def only_loaded(self, mapper: Callable) -> dict:
        rel_name = self._get_mapper_param(mapper)
        relation = getattr(self, rel_name)
        return {} if not relation.load_entity_list().is_loaded() else {
            rel_name: mapper(relation)
        }


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
