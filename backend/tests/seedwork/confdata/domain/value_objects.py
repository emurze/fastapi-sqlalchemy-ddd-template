import uuid
from typing import NewType

from seedwork.domain.value_objects import ValueObject

ExampleId = NewType("ExampleId", uuid.UUID)
ExampleItemId = NewType("ExampleItemId", uuid.UUID)
PostId = NewType("PostId", uuid.UUID)
UserId = NewType("UserId", uuid.UUID)
PermissionId = NewType("PermissionId", uuid.UUID)


class Address(ValueObject):
    city: str


class Photo(ValueObject):
    url: str
    context: str
