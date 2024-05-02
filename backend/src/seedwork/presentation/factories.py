from collections.abc import Callable

from seedwork.application.messagebus import (
    Message,
    MessageBus,
    HandlerWithParams,
)
from seedwork.utils.functional import get_first_param_type


def get_bus(
    query_handlers: dict[type[Message], HandlerWithParams],
    command_handlers: dict[type[Message], HandlerWithParams],
    event_handlers: dict[type[Message], HandlerWithParams],
) -> MessageBus:
    return MessageBus(
        query_handlers=query_handlers,
        command_handlers=command_handlers,
        event_handlers=event_handlers,
    )


def get_dict(*handlers: dict) -> dict[type[Message], HandlerWithParams]:
    return {msg: (handler, args, kw) for msg, handler, args, kw in handlers}


def get_handler(handler, *args, **kw) -> tuple[Message, Callable, tuple, dict]:
    return get_first_param_type(handler), handler, args, kw
