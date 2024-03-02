from dataclasses import dataclass
from datetime import datetime
from typing import Optional, NewType

from shared.domain.entities import AggregateRoot

ClientId = NewType("ClientId", int)


@dataclass(kw_only=True)
class Client(AggregateRoot[ClientId]):
    username: str
    date_joined: datetime
    last_login: Optional[datetime] = None
