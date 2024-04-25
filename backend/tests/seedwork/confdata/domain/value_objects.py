import uuid
from typing import NewType

from seedwork.domain.value_objects import ValueObject

ExampleId = NewType('ExampleId', uuid.UUID)
ExampleItemId = NewType('ExampleItemId', uuid.UUID)
PostId = NewType('PostId', uuid.UUID)
CommentId = NewType('CommentId', uuid.UUID)


class Address(ValueObject):
    city: str
