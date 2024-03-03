import abc

from shared.application.commands import Command, CommandResult


class ICommandHandler(abc.ABC):
    @abc.abstractmethod
    async def execute(self, command: Command) -> CommandResult: ...
