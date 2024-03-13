import abc

from shared.application.dtos import Model, OutputDto


class Event(Model):
    pass


class IEventHandler(abc.ABC):
    @abc.abstractmethod
    async def handle(self, event: Event) -> OutputDto:
        ...
