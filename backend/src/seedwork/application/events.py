from typing import Optional

from seedwork.application.dtos import DTO
from seedwork.domain.errors import Error
from seedwork.domain.events import DomainEvent


class EventResult(DTO):
    events: list[DomainEvent] = []
    error: Optional[Error] = None

    def is_success(self):
        return not self.error

    def is_failure(self) -> bool:
        return not self.is_success()
