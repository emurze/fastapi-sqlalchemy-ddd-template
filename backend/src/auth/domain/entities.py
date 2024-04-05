from pydantic import Field

from auth.application.event.notify_developers import NameChanged
from auth.domain.value_objects import AccountId
from seedwork.domain.entities import AggregateRoot
from seedwork.domain.value_objects import Deferred, deferred


class Account(AggregateRoot):
    id: deferred[AccountId] = Deferred
    name: str = Field(max_length=128)

    def publish(self) -> None:
        self.register_event(NameChanged(name=self.name))
