from dataclasses import dataclass, field
from typing import NoReturn, TypeAlias, Callable, Annotated

from typing_extensions import Doc

from seedwork.application.commands import Command, CommandResult
from seedwork.application.events import EventResult
from seedwork.application.queries import Query, QueryResult
from seedwork.domain.events import DomainEvent

Message: TypeAlias = Command | Query | DomainEvent
Result: TypeAlias = CommandResult | QueryResult | EventResult


@dataclass(slots=True)
class MessageBus:
    command_handlers: dict[type[Command], Callable]
    query_handlers: dict[type[Query], Callable]
    event_handlers: dict[type[DomainEvent], Callable]
    queue: Annotated[
        list,
        Doc(
            """
            Queue contains domain events.
            """
        )
    ] = field(default_factory=list)
    background_queue: Annotated[
        list,
        Doc(
            """
            Background queue contains integration (async) events to cross 
            bounded contexts.
            """
        )
    ] = field(default_factory=list)

    async def handle(self, message: Message) -> NoReturn | Result:
        if isinstance(message, Command):
            return await self._handle_command(message)
        elif isinstance(message, Query):
            return await self._handle_query(message)
        else:
            raise TypeError("Param type isn't in (Command, Query, Event)")

    async def _handle_command(self, command: Command) -> CommandResult:
        handler = self.command_handlers[type(command)]
        result, uow = await handler(command)
        self.queue += uow.collect_events()
        self.background_queue += result.events

        print(f"{self.queue=}")
        print(f"{self.background_queue=}")

        while len(self.queue) > 0:
            event_result = await self._handle_domain_event(self.queue.pop(0))
            self.queue += event_result.events

        return result

    async def _handle_query(self, query: Query) -> QueryResult:
        handler = self.query_handlers[type(query)]
        result, _ = await handler(query)
        return result

    async def _handle_domain_event(self, event: DomainEvent) -> EventResult:
        handler = self.event_handlers[type(event)]
        return await handler(event)
