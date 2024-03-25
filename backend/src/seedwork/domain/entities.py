from pydantic import ConfigDict, BaseModel

from seedwork.domain.value_objects import Deferred, deferred


class Entity(BaseModel):
    model_config = ConfigDict(validate_assignment=True)
    id: deferred[int] = Deferred

    def update(self, **kw) -> None:
        assert kw.get("id") is None, "Entity can't update its identity."
        for key, value in kw.items():
            setattr(self, key, value)


class LocalEntity(Entity):
    """Entity inside an aggregate."""


class AggregateRoot(Entity):
    """Consists of 1+ entities. Spans transaction boundaries."""

    # EVENT COLLECTION
