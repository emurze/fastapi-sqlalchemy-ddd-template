from typing import Any, TypeVar, Generic, cast

from pydantic import ConfigDict, BaseModel
from pydantic.fields import FieldInfo

from seedwork.domain.events import Event
from seedwork.utils.functional import classproperty

EntityId = TypeVar("EntityId")  # UUID


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


class Entity(BaseModel, Generic[EntityId]):
    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        arbitrary_types_allowed=True,
    )
    id: EntityId

    @classproperty
    def c(self) -> EntityWrapper:
        cls = cast(type[BaseModel], self)
        return EntityWrapper(cls)

    def update(self, **kw) -> None:
        assert kw.get("id") is None, "Entity can't update its identity."
        for key, value in kw.items():
            setattr(self, key, value)

    def __str__(self) -> str:
        return f"{type(self).__name__}({', '.join(super().__str__().split())})"


class LocalEntity(Entity):
    """Entity inside an aggregate."""


class AggregateRoot(Entity[EntityId]):
    """Consists of 1+ entities. Spans transaction boundaries."""

    _events: list[Event] = []

    def register_event(self, event: Event) -> None:
        self._events.append(event)

    def collect_events(self) -> list[Event]:
        events = self._events
        self._events = []
        return events
