from pydantic import Field

from seedwork.domain.entities import AggregateRoot
from seedwork.domain.value_objects import defer, Deferred
from tests.seedwork.confdata.domain.events import NameChanged
from tests.seedwork.confdata.domain.value_objects import ExampleId


class Example(AggregateRoot):
    id: defer[ExampleId] = Deferred
    name: str = Field(max_length=10)

    def change_name(self, new_name: str) -> None:
        self.name = new_name
        self.register_event(NameChanged(new_name=new_name))
