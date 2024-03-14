import inspect
from functools import partial
from typing import TypeAlias, Callable

from dependency_injector import providers


def _link(obj):
    return providers.Singleton(lambda: obj)


def _group(*singletons):
    def inner(*args) -> list:
        return list(args)

    return providers.Singleton(inner, *singletons)


def _inject_in_handler(handler: Callable, *args, **kw):
    def wrapper(message):
        return handler(message, *args, **kw)

    return _link((wrapper, handler))

    # handler(command, uow=3)


Link: TypeAlias = _link
Group: TypeAlias = _group
InjectInHandler: TypeAlias = _inject_in_handler
