from typing import Any

from seedwork.application.dtos import DTO
from seedwork.domain.errors import Error, NoneError
from seedwork.domain.events import Event


class Query(DTO):
    pass


class QueryResult(DTO):
    payload: Any = None
    events: list[Event] = []
    error: Error | NoneError = NoneError
