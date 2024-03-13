import abc

from shared.application.dtos import OutputDto
from shared.domain.events import Event


class IEventHandler(abc.ABC):
    @abc.abstractmethod
    async def handle(self, event: Event) -> OutputDto:
        ...
