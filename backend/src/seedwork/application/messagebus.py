from dataclasses import dataclass, field
from typing import NoReturn, TypeAlias, Callable

from seedwork.application.commands import Command, CommandResult
from seedwork.application.events import EventResult
from seedwork.application.queries import Query, QueryResult
from seedwork.domain.events import Event
from seedwork.domain.uows import IUnitOfWork

Message: TypeAlias = Command | Query | Event
Result: TypeAlias = CommandResult | QueryResult | EventResult


@dataclass(frozen=True, slots=True)
class MessageBus:
    uow: IUnitOfWork
    command_handlers: dict[type[Command], Callable]
    query_handlers: dict[type[Query], Callable]
    event_handlers: dict[type[Event], Callable]
    queue: list = field(default_factory=list)

    async def handle(self, new_message: Message) -> NoReturn | Result:
        self.queue.append(new_message)
        while self.queue:
            message = self.queue.pop(0)
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
        self.queue += self.uow.collect_events()
        return await handler(command)

    async def _handle_query(self, query: Query) -> QueryResult:
        handler = self.query_handlers[type(query)]
        return await handler(query)

    async def _handle_event(self, event: Event) -> EventResult:
        handler = self.event_handlers[type(event)]
        return await handler(event)
