import itertools as it
from collections.abc import Iterator
from datetime import datetime
from collections.abc import Callable
from dataclasses import field
from inspect import signature
from typing import Any, TypeVar

from pydantic import BaseModel


def get_first_param_type(func: Callable):
    handler_signature = signature(func)
    kwargs_iterator = iter(handler_signature.parameters.items())
    _, first_param = next(kwargs_iterator)
    return first_param.annotation


def invisible_field(default_factory: Callable):
    return field(
        init=False, repr=False, compare=False, default_factory=default_factory
    )


class classproperty(property):  # noqa
    def __get__(self, cls, owner):  # noqa
        return classmethod(self.fget).__get__(None, owner)()  # noqa


T = TypeVar("T")


def mixin_for(_: T) -> T:
    return object


def id_int_gen() -> Iterator[int]:
    return it.count(start=1)


def create_at_gen() -> Iterator[datetime]:
    while True:
        yield datetime.utcnow()
