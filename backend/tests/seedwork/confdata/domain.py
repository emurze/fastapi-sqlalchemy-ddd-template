import uuid
from typing import NewType

from pydantic import Field

from seedwork.domain.async_structs import alist
from seedwork.domain.entities import AggregateRoot, LocalEntity
from seedwork.domain.events import Event
from seedwork.domain.services import UUIDField
from seedwork.domain.value_objects import ValueObject

AddressId = NewType('AddressId', uuid.UUID)
ExampleId = NewType('ExampleId', uuid.UUID)
ExampleItemId = NewType('ExampleItemId', uuid.UUID)


class NameChanged(Event):
    new_name: str


class Example(AggregateRoot):
    id: ExampleId = UUIDField
    name: str = Field(max_length=10)
    items: alist['ExampleItem'] = alist()

    def change_name(self, new_name: str) -> None:
        self.name = new_name
        self.register_event(NameChanged(new_name=new_name))


class ExampleItem(LocalEntity):
    id: ExampleItemId = UUIDField
    name: str
    addresses: alist['Address'] = alist()


class Address(ValueObject):
    id: AddressId = UUIDField
    city: str
