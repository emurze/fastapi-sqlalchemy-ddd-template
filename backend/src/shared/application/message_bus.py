from dataclasses import dataclass
from typing import NoReturn

from shared.application.commands import ICommandHandler, Command
from shared.application.dtos import OutputDto
from shared.application.queries import IQueryHandler, Query

Message = Command | Query


@dataclass(frozen=True, slots=True)
class MessageBus:
    command_handlers: dict[type[Command], ICommandHandler]
    query_handlers: dict[type[Query], IQueryHandler]

    async def handle(self, message: Message) -> NoReturn | OutputDto:
        if isinstance(message, Command):
            handler = self.command_handlers[message.__class__]
            return await handler.handle(message)

        elif isinstance(message, Query):
            handler = self.query_handlers[message.__class__]
            return await handler.handle(message)

        else:
            raise TypeError("Param type isn't in [Command, Query, Event]")
