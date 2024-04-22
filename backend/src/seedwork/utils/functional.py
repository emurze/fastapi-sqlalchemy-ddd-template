from collections.abc import Callable
from dataclasses import field
from inspect import signature
from typing import TypeVar

T = TypeVar("T")
OnlySingleParamMessage = "Callback should have only one parameter."


def get_first_param_type(func: Callable):
    handler_signature = signature(func)
    kwargs_iterator = iter(handler_signature.parameters.items())
    _, first_param = next(kwargs_iterator)
    return first_param.annotation


def get_single_param(
    mapper: Callable,
    message: str = OnlySingleParamMessage,
) -> str:
    res = signature(mapper)
    params = tuple(res.parameters)
    assert len(params) == 1, message
    return params[0]


def invisible_field(default_factory: Callable):
    return field(
        init=False, repr=False, compare=False, default_factory=default_factory
    )


class classproperty(property):  # noqa
    def __get__(self, cls, owner):  # noqa
        return classmethod(self.fget).__get__(None, owner)()  # noqa
