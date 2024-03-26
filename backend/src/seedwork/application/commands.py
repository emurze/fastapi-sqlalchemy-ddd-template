from dataclasses import dataclass, field
from typing import Any

from seedwork.application.dtos import DTO
from seedwork.domain.errors import Error, NoneError
from seedwork.domain.events import Event


class Command(DTO):
    pass


@dataclass(kw_only=True)
class CommandResult(DTO):
    payload: Any = None
    events: list[Event] = field(default_factory=list)
    error: Error | NoneError = NoneError
