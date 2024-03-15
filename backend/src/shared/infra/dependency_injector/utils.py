from typing import TypeAlias, Callable

from dependency_injector import providers
from dependency_injector.providers import Singleton


def _link(obj):
    return providers.Singleton(lambda: obj)


def _group(*singletons):
    def inner(*args) -> list:
        return list(args)

    return providers.Singleton(inner, *singletons)


def _inject_in(func: Callable, *args, **kw):
    def wrapper(message):
        _args = (a() if isinstance(a, Singleton) else a for a in args)
        return func(message, *_args, **kw)

    return _link((wrapper, func))


Link: TypeAlias = _link
Group: TypeAlias = _group
InjectIn: TypeAlias = _inject_in
