from typing import Any, Optional

from seedwork.application.dtos import DTO
from seedwork.domain.errors import Error
from seedwork.domain.events import Event


class Command(DTO):
    pass


class CommandResult(DTO):
    payload: Any = None
    events: list[Event] = []
    error: Optional[Error] = None
