from typing import Self, Any

from shared.domain.pydantic_v1 import py_dataclass
from shared.domain.value_objects import Deferred, deferred


class EntityConfig:
    validate_assignment = True


@py_dataclass(config=EntityConfig)
class Entity:
    id: deferred[int] = Deferred

    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def update(self, **kw) -> None:
        assert kw.get("id") is None, "Entity can't update its identity."
        for key, value in kw.items():
            setattr(self, key, value)

    @classmethod
    def get_dict_from(cls, obj: Any) -> dict:
        """
        Ignores deferred fields
        """
        return {
            attr: value
            for attr in cls.__dataclass_fields__  # noqa
            if (value := getattr(obj, attr)) != Deferred
        }

    @classmethod
    def model_from(cls, obj: Any) -> Self:
        return cls(**cls.get_dict_from(obj))

    def as_dict(self) -> dict:
        return self.get_dict_from(self)


@py_dataclass(kw_only=True)
class AggregateRoot(Entity):
    """Consists of 1+ entities. Spans transaction boundaries."""

    # EVENT COLLECTION
