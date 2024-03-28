from typing import TypeAlias

from dependency_injector import providers


def _link(obj):
    return providers.Singleton(lambda: obj)


Link: TypeAlias = _link
