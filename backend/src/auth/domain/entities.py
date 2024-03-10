from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from shared.domain.entities import AggregateRoot


@dataclass(kw_only=True)
class Client(AggregateRoot):
    username: str
    date_joined: datetime
    last_login: Optional[datetime] = None
