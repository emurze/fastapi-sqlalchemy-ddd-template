import itertools as it
from collections.abc import Iterator
from datetime import datetime
from collections.abc import Callable
from dataclasses import field
from inspect import signature
from typing import Any

from pydantic import BaseModel


def get_first_param_annotation(func: Callable):
    handler_signature = signature(func)
    kwargs_iterator = iter(handler_signature.parameters.items())
    _, first_param = next(kwargs_iterator)
    return first_param.annotation


def invisible_field(default_factory: Callable):
    return field(
        init=False, repr=False, compare=False, default_factory=default_factory
    )


def get_const(model: type[BaseModel], path: str) -> Any:
    _field_name, constraint_name = path.split('.')
    _field = model.model_fields[_field_name]

    for item in _field.metadata:
        value = getattr(item, constraint_name)
        return value


def id_int_gen() -> Iterator[int]:
    return it.count(start=1)


def create_at_gen() -> Iterator[datetime]:
    while True:
        yield datetime.utcnow()
