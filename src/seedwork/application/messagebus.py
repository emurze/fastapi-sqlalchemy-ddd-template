from collections.abc import Callable
from dataclasses import dataclass, field
from functools import partial
from typing import TypeAlias, NoReturn

from seedwork.application.commands import Command, CommandResult
from seedwork.application.events import EventResult
from seedwork.application.queries import Query, QueryResult
from seedwork.domain.errors import Error
from seedwork.domain.events import DomainEvent
from seedwork.domain.uows import IBaseUnitOfWork

Handler: TypeAlias = dict[Callable, tuple, dict]
Message: TypeAlias = Command | Query
Result: TypeAlias = CommandResult | QueryResult


@dataclass(slots=True)
class MessageBus:
    """A context spanning a single transaction for execution of commands and queries

    Typically, the following thing happen in message bus:
    - a command handler is called, which results in aggregate changes that fire domain events
    - a domain event is raised, after
    - a domain event handler is called
    - a command is executed
    """

    command_handlers: dict[type[Command], Handler]
    event_handlers: dict[type[DomainEvent], list[Handler]]
    query_handlers: dict[type[Query], Handler]
    event_queue: list[DomainEvent] = field(default_factory=list)

    async def handle(self, message: Message) -> NoReturn | Result:
        if isinstance(message, Command):
            return await self._handle_command(message)
        elif isinstance(message, Query):
            return await self._handle_query(message)
        else:
            raise ValueError("Input must be a Command or a Query.")

    async def _handle_command(self, command: Command) -> CommandResult:
        handler, args, kw = self.command_handlers[type(command)]
        uow_factory = kw["uow"]
        async with uow_factory() as uow:
            wrapper_handler = partial(handler, *args, **(kw | {"uow": uow}))
            result = await wrapper_handler(command)
            if isinstance(result, CommandResult):
                res = result
            elif isinstance(result, Error):
                await uow.rolback()
                return CommandResult(error=result)
            else:
                res = CommandResult(payload=result)

            await self._run_event_queue(uow)
            await uow.commit()
            return res

    async def _run_event_queue(self, uow: IBaseUnitOfWork):
        self.event_queue += uow.collect_events()
        while len(self.event_queue) > 0:
            event = self.event_queue.pop(0)
            events_or_error = await self._handle_domain_event(event, uow)
            if isinstance(events_or_error, Error):
                await uow.rollback()
                return CommandResult(error=events_or_error)
            else:
                self.event_queue += events_or_error

    async def _handle_domain_event(
        self, event: DomainEvent, uow: IBaseUnitOfWork
    ) -> list[EventResult] | Error:
        all_events = []
        for handler, args, kw in self.event_handlers[type(event)]:
            kw = kw.copy() | {"uow": uow} if kw.get("uow") else kw
            result = await handler(event, *args, **kw)
            if isinstance(result, Error):
                return result
            else:
                all_events += uow.collect_events()
        return all_events

    async def _handle_query(self, query: Query) -> QueryResult:
        handler, args, kw = self.query_handlers[type(query)]
        async with kw["session"]() as session:
            kw = kw | {"session": session}
            wrapped_handler = partial(handler, *args, **kw)
            result = await wrapped_handler(query)
            if isinstance(result, Error):
                return QueryResult(error=result)
            else:
                return QueryResult(payload=result)
