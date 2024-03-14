from dataclasses import dataclass
from typing import NoReturn, TypeAlias, Callable

from shared.application.commands import Command, CommandResult
from shared.application.events import EventResult
from shared.application.queries import Query, QueryResult
from shared.domain.events import Event

Message: TypeAlias = Command | Query | Event
Result: TypeAlias = CommandResult | QueryResult | EventResult


@dataclass(frozen=True, slots=True)
class MessageBus:
    command_handlers: dict[type[Command], Callable]
    query_handlers: dict[type[Query], Callable]
    event_handlers: dict[type[Event], Callable]

    async def handle(self, message: Message) -> NoReturn | Result:
        if isinstance(message, Command):
            return await self._handle_command(message)
        elif isinstance(message, Query):
            return await self._handle_query(message)
        elif isinstance(message, Event):
            return await self._handle_event(message)
        else:
            raise TypeError("Param type isn't in [Command, Query, Event]")

    async def _handle_command(self, command: Command) -> CommandResult:
        handler = self.command_handlers[type(command)]
        return await handler(command)

    async def _handle_query(self, query: Query) -> QueryResult:
        handler = self.query_handlers[type(query)]
        return await handler(query)

    async def _handle_event(self, event: Event) -> EventResult:
        handler = self.event_handlers[type(event)]
        return await handler(event)
