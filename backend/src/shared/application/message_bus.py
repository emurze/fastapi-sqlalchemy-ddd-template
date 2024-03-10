from dataclasses import dataclass
from typing import NoReturn, TypeAlias

from shared.application.commands import ICommandHandler, Command
from shared.application.dtos import OutputDto
from shared.application.queries import IQueryHandler, Query

Message: TypeAlias = Command | Query


@dataclass(frozen=True, slots=True)
class MessageBus:
    command_handlers: dict[type[Command], ICommandHandler]
    query_handlers: dict[type[Query], IQueryHandler]

    async def handle(self, message: Message) -> NoReturn | OutputDto:
        if isinstance(message, Command):
            return await self._handle_command(message)
        elif isinstance(message, Query):
            return await self._handle_query(message)
        else:
            raise TypeError("Param type isn't in [Command, Query, Event]")

    async def _handle_command(self, command: Command) -> OutputDto:
        handler = self.command_handlers[type(command)]
        return await handler.handle(command)

    async def _handle_query(self, query: Query) -> OutputDto:
        handler = self.query_handlers[type(query)]
        return await handler.handle(query)
