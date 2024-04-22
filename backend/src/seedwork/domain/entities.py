from collections.abc import Callable
from typing import Any, cast
from uuid import UUID

from pydantic import ConfigDict, BaseModel
from pydantic.fields import FieldInfo, PrivateAttr

from seedwork.domain.events import DomainEvent
from seedwork.domain.services import UUIDField
from seedwork.domain.structs import alist, ListAction
from seedwork.utils.functional import classproperty, get_single_param


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

    def only_loaded(self, mapper: Callable) -> dict:
        relation = getattr(self, name := get_single_param(mapper))
        return {} if not relation.load_entity_list().is_loaded() else {
            name: mapper(relation)
        }

    def _add_new_model(self):
        pass

    def _persist_relation(self, entity_relation, model_relation, mapper):
        """Executes actions"""
        for action_name, value in entity_relation._actions.items():
            match action_name:
                case ListAction.APPEND:
                    model_relation.append(mapper(value))
                case ListAction.POP:
                    model_relation.pop(mapper(value))

    def add_or_persist_changes(
        self,
        rel_name: str,
        model_relation: list,
        entity_relation: alist,
        mapper: Callable
    ) -> dict:
        if not entity_relation.load_entity_list().is_loaded():
            return {}

        if entity_relation._sync_list:
            self._add_new_model()
        else:
            self._persist_relation(entity_relation, model_relation, mapper)


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
