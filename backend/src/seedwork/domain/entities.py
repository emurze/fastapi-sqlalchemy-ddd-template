from typing import Iterator, Any, TypeVar, Generic, Self

from pydantic import ConfigDict, BaseModel
from pydantic.fields import FieldInfo

from seedwork.domain.events import Event
from seedwork.domain.value_objects import Deferred, deferred
from seedwork.utils.functional import classproperty

EntityId = TypeVar("EntityId")


class Column:
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
        return Column(self._entity.model_fields[field_name], self._entity)

    def __getitem__(self, field_name: str) -> Any:
        return self.__getattr__(field_name)


class Entity(BaseModel, Generic[EntityId]):
    model_config = ConfigDict(validate_assignment=True, from_attributes=True)
    id: deferred[EntityId] = Deferred

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

    @classproperty
    def c(self: type[Self]) -> EntityWrapper:
        return EntityWrapper(self)

    def update(self, **kw) -> None:
        assert kw.get("id") is None, "Entity can't update its identity."
        for key, value in kw.items():
            setattr(self, key, value)

    def __str__(self) -> str:
        default_str = super().__str__()
        return f"{type(self).__name__}({', '.join(default_str.split())})"


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
