from pydantic import Field

from iam.domain.value_objects import AccountId
from seedwork.domain.entities import AggregateRoot


class Account(AggregateRoot):
    id: AccountId
    name: str = Field(max_length=128)
