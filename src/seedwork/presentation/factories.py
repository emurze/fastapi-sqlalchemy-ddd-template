from collections.abc import Callable

from dependency_injector import providers

from seedwork.application.messagebus import Message
from seedwork.utils.functional import get_first_param_type

Handler = tuple[Callable, tuple, dict]


def make_singleton(func: Callable) -> Callable:
    def inner(*args, **kw):
        return providers.Singleton(func, *args, **kw)

    return inner


def get_dict(*handlers: dict) -> dict[type[Message], Handler]:
    return {msg: (handler, args, kw) for msg, (handler, args, kw) in handlers}


def get_event_list(*handlers: dict):
    event_handlers = {}
    for message, (handler, args, kw) in handlers:
        if event_handlers.get(message):
            event_handlers[message].append((handler, args, kw))
        else:
            event_handlers[message] = [(handler, args, kw)]
    return event_handlers


def get_handler(handler, *args, **kw) -> tuple[Message, Handler]:
    return get_first_param_type(handler), (handler, args, kw)


DictSingleton = make_singleton(get_dict)
HandlerSingleton = make_singleton(get_handler)
EventListSingleton = make_singleton(get_event_list)
