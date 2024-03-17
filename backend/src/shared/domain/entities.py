from shared.domain.pydantic_v1 import dataclass
from shared.domain.value_objects import Deferred, deferred


class EntityConfig:
    validate_assignment = True


@dataclass(config=EntityConfig)
class Entity:
    id: deferred[int] = Deferred

    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def update(self, **kw) -> None:
        assert kw.get("id") is None, "Entity can't update its identity."
        for key, value in kw.items():
            setattr(self, key, value)

    def as_dict(self) -> dict:
        """
        Ignore deferred fields
        """
        return {
            attr: value
            for attr in self.__dataclass_fields__  # noqa
            if (value := getattr(self, attr)) != Deferred
                and not attr.startswith("_")
        }


@dataclass(kw_only=True)
class AggregateRoot(Entity):
    """Consists of 1+ entities. Spans transaction boundaries."""

    # EVENT COLLECTION
