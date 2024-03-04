import abc
from collections.abc import Awaitable
from typing import Any


class ICacheClient(abc.ABC):
    @abc.abstractmethod
    async def get(self, key: str) -> Awaitable[Any]: ...

    @abc.abstractmethod
    async def set(self, key: str, value: Any, lifetime: int) -> None: ...
