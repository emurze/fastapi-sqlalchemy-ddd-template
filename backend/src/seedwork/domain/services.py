import uuid

from pydantic import Field


def next_id() -> uuid.UUID:
    return uuid.uuid4()


UUIDField = Field(default_factory=next_id, frozen=True)
