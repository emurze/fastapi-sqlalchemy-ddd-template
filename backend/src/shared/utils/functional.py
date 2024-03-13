import inspect
from collections.abc import Callable
from dataclasses import field, Field


def get_first_param_annotation(func: Callable):
    handler_signature = inspect.signature(func)
    kwargs_iterator = iter(handler_signature.parameters.items())
    _, first_param = next(kwargs_iterator)
    return first_param.annotation


def invisible_field(default_factory: Callable) -> Field:
    return field(
        init=False, repr=False, compare=False, default_factory=default_factory
    )
