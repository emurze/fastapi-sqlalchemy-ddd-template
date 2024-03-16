from pydantic.dataclasses import dataclass

from shared.domain.value_objects import Deferred, deferred


@dataclass(kw_only=True)
class Entity:
    """
    1. Transit carefully to presentation layer
    2. Write logic to return presentation error
    """

    id: deferred[int] = Deferred

    def __init__(self, **kw) -> None:
        super().__init__(**kw)

    def update(self, **kw) -> None:
        assert kw.get("id") is None, "Entity can't update id"
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

    # events: list = invisible_field(default_factory=list)
    #
    # def register_event(self, event: Event) -> None:
    #     self.events.append(event)
    #
    # def collect_events(self):
    #     pass


