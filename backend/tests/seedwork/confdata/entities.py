from pydantic import Field

from seedwork.domain.entities import AggregateRoot
from seedwork.domain.value_objects import deferred, Deferred
from tests.seedwork.confdata.events import NameChanged
from tests.seedwork.confdata.value_objects import ExampleId


class Example(AggregateRoot):
    id: deferred[ExampleId] = Deferred
    name: str = Field(max_length=10)

    def change_name(self, new_name: str) -> None:
        self.name = new_name
        self.register_event(NameChanged(new_name=new_name))
