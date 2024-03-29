from auth.domain.value_objects import AccountId
from seedwork.domain.entities import AggregateRoot
from seedwork.domain.value_objects import Deferred, deferred


class Account(AggregateRoot):
    id: deferred[AccountId] = Deferred
