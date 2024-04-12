import uuid
from typing import NewType

from pydantic import Field

from seedwork.domain.entities import AggregateRoot
from seedwork.domain.events import Event
from seedwork.domain.services import UUIDField

ExampleId = NewType('ExampleId', uuid.UUID)


class NameChanged(Event):
    new_name: str


class Example(AggregateRoot):
    id: ExampleId = UUIDField
    name: str = Field(max_length=10)

    def change_name(self, new_name: str) -> None:
        self.name = new_name
        self.register_event(NameChanged(new_name=new_name))
