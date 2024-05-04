import uuid
from dataclasses import dataclass
from typing import NewType

ExampleId = NewType("ExampleId", uuid.UUID)
ExampleItemId = NewType("ExampleItemId", uuid.UUID)


@dataclass(kw_only=True, frozen=True)
class Address:
    city: str
