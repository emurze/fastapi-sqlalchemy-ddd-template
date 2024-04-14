import uuid
from typing import NewType

from pydantic import Field

from seedwork.domain.entities import AggregateRoot, LocalEntity
from seedwork.domain.events import Event
from seedwork.domain.services import UUIDField
from seedwork.domain.value_objects import ValueObject

ExampleId = NewType('ExampleId', uuid.UUID)
ExampleItemId = NewType('ExampleItemId', uuid.UUID)
AddressId = NewType('AddressId', uuid.UUID)


class NameChanged(Event):
    new_name: str


class Example(AggregateRoot):
    id: ExampleId = UUIDField
    name: str = Field(max_length=10)

    def change_name(self, new_name: str) -> None:
        self.name = new_name
        self.register_event(NameChanged(new_name=new_name))


class ExampleItem(LocalEntity):
    id: ExampleItemId = UUIDField
    name: str


class Address(ValueObject):
    id: AddressId = UUIDField
    city: str
