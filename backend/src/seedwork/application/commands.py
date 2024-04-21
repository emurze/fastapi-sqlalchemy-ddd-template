from typing import Any, Optional

from seedwork.application.dtos import DTO
from seedwork.domain.errors import Error
from seedwork.domain.events import DomainEvent


class Command(DTO):
    pass


class CommandResult(DTO):
    payload: Any = None
    events: list[DomainEvent] = []
    error: Optional[Error] = None

    def is_success(self):
        return not self.error
