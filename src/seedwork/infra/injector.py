from collections.abc import Callable
from typing import Any

from dependency_injector import providers


def _link(obj: Any) -> Callable:
    return providers.Singleton(lambda: obj)


Link: Callable = _link
