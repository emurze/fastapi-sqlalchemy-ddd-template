import inspect
from collections.abc import Callable


def get_first_param_annotation(func: Callable):
    handler_signature = inspect.signature(func)
    kwargs_iterator = iter(handler_signature.parameters.items())
    _, first_param = next(kwargs_iterator)
    return first_param.annotation
