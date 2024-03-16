from collections.abc import Callable
from dataclasses import field
from inspect import signature


def get_first_param_annotation(func: Callable):
    handler_signature = signature(func)
    kwargs_iterator = iter(handler_signature.parameters.items())
    _, first_param = next(kwargs_iterator)
    return first_param.annotation


def invisible_field(default_factory: Callable):
    return field(
        init=False, repr=False, compare=False, default_factory=default_factory
    )


def get_const(_field, name: str):
    for const in _field.metadata:
        if const_value := getattr(const, name):
            return const_value
