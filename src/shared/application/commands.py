import abc

from pydantic import BaseModel, ConfigDict


class Command(BaseModel):
    pass


class CommandResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ICommandHandler(abc.ABC):
    @abc.abstractmethod
    async def execute(self, command: Command) -> CommandResult: ...
