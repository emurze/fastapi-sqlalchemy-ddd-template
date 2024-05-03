from collections.abc import Callable
from dataclasses import dataclass, field
from functools import partial
from typing import NoReturn, TypeAlias

from seedwork.application.commands import Command, CommandResult
from seedwork.application.events import EventResult
from seedwork.application.queries import Query, QueryResult
from seedwork.domain.errors import Error
from seedwork.domain.events import DomainEvent

HandlerWithParams: TypeAlias = tuple[Callable, tuple, dict]
Message: TypeAlias = Command | Query | DomainEvent
Result: TypeAlias = CommandResult | QueryResult | EventResult


@dataclass(slots=True)
class MessageBus:
    command_handlers: dict[type[Command], HandlerWithParams]
    event_handlers: dict[type[DomainEvent], HandlerWithParams]
    query_handlers: dict[type[Query], HandlerWithParams]
    queue: list = field(default_factory=list)
    background_queue: list = field(default_factory=list)

    async def handle(self, message: Message) -> NoReturn | Result:
        if isinstance(message, Command):
            return await self._handle_command(message)
        elif isinstance(message, Query):
            return await self._handle_query(message)
        else:
            raise TypeError("Param type isn't a Command or a Query.")

    async def _handle_command(self, command: Command) -> CommandResult:
        handler, args, kw = self.command_handlers[type(command)]

        uow_factory = kw["uow"]
        async with uow_factory() as uow:
            wrapper_handler = partial(handler, *args, **(kw | {"uow": uow}))
            result = await wrapper_handler(command)

            if isinstance(result, Error):
                return CommandResult(error=result)

            self.queue += uow.collect_events()

            if result:
                self.background_queue += result.events

            while len(self.queue) > 0:
                event = self.queue.pop(0)
                event_result = await self._handle_domain_event(event)
                self.queue += event_result.events

            await uow.commit()

        return CommandResult(payload=result)

    async def _handle_query(self, query: Query) -> QueryResult:
        handler, args, kw = self.query_handlers[type(query)]

        new_kw = {}
        if session_factory := kw.get("session"):
            new_kw = kw.copy()
            new_kw["session"] = session_factory()

        wrapper_handler = partial(handler, *args, **(new_kw or kw))
        result = await wrapper_handler(query)

        if session := new_kw.get("session"):
            await session.close()

        if isinstance(result, QueryResult):
            return result

        if isinstance(result, Error):
            return QueryResult(error=result)

        return QueryResult(payload=result)

    async def _handle_domain_event(self, event: DomainEvent) -> EventResult:
        handler, args, kw = self.event_handlers[type(event)]
        wrapper_handler = partial(handler, *args, **kw)
        return await wrapper_handler(event)
