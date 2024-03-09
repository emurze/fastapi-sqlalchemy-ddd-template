import abc

from shared.application.dtos import Model, Result


class Command(Model):
    pass


class ICommandHandler(abc.ABC):
    @abc.abstractmethod
    async def handle(self, command: Command) -> Result:
        ...
