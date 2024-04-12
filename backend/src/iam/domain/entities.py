from pydantic import Field

from iam.domain.value_objects import AccountId
from seedwork.domain.entities import AggregateRoot
from seedwork.domain.services import UUIDField


class Account(AggregateRoot):
    id: AccountId = UUIDField
    name: str = Field(max_length=128)
