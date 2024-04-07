from pydantic import Field

from auth.domain.value_objects import AccountId
from seedwork.domain.entities import AggregateRoot
from seedwork.domain.value_objects import Deferred, defer


class Account(AggregateRoot):
    id: defer[AccountId] = Deferred
    name: str = Field(max_length=128)
