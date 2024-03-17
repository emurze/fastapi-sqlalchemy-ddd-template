from dataclasses import dataclass, field
from typing import Any

from shared.application.dtos import DTO
from shared.domain.errors import Error, NoneError
from shared.domain.events import Event


class Query(DTO):
    pass


@dataclass(kw_only=True)
class QueryResult(DTO):
    payload: Any = None
    events: list[Event] = field(default_factory=list)
    error: Error | NoneError = NoneError
