from dataclasses import dataclass, field
from typing import Any, Optional

from shared.application.utils import DataclassMixin
from shared.domain.errors import Error, NoneError
from shared.domain.events import Event


class Query(DataclassMixin):
    pass


@dataclass
class QueryResult(DataclassMixin):
    payload: Any = None
    events: list[Event] = field(default_factory=list)
    error: Error | NoneError = NoneError
