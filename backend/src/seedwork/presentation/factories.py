from collections.abc import Callable
from typing import TypeAlias

from seedwork.application.messagebus import Message, MessageBus, Result
from seedwork.utils.functional import get_first_param_type
from shared.domain.uow import IUnitOfWork

WrappedHandler: TypeAlias = Callable


def get_bus(
    query_handlers: dict[type[Message], WrappedHandler],
    command_handlers: dict[type[Message], WrappedHandler],
    event_handlers: dict[type[Message], WrappedHandler],
) -> MessageBus:
    return MessageBus(
        query_handlers=query_handlers,
        command_handlers=command_handlers,
        event_handlers=event_handlers,
    )


def get_dict(*handlers: dict) -> dict[type[Message], WrappedHandler]:
    return {k: v for handler in handlers for k, v in handler.items()}


def get_handler(handler, *args, **kw) -> dict[type[Message], WrappedHandler]:
    async def wrapper(message: Message) -> tuple[Result, IUnitOfWork]:
        """
        Wraps the provided handler function to accept a message
        and ensures the creation of a new unit of work
        if a factory with "uow" name is provided.
        """

        new_kw = None
        uow = None

        if uow_factory := kw.get('uow'):
            uow = uow_factory()
            new_kw = kw.copy()
            new_kw['uow'] = uow

        return await handler(message, *args, **(new_kw or kw)), uow

    return {get_first_param_type(handler): wrapper}
