from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from shared.domain.entities import AggregateRoot
from shared.domain.value_objects.lazy import lazy, metadata


@dataclass(kw_only=True)
class Client(AggregateRoot):
    username: str
    date_joined: lazy[datetime] = metadata('auto-update')
    last_login: Optional[datetime] = None
