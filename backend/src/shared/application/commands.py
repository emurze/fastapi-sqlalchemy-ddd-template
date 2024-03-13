import abc

from shared.application.dtos import Model, OutputDto


class Command(Model):
    pass


class ICommandHandler(abc.ABC):
    @abc.abstractmethod
    async def handle(self, command: Command) -> OutputDto: ...
