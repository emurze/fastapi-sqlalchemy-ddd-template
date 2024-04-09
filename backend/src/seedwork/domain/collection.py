from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TypeVar, Generic, Optional, TypeAlias, Any

T = TypeVar('T')


@dataclass
class _AsyncList(Generic[T]):
    list_: list[T] = field(default_factory=list)
    coro: Optional[Callable] = None

    def __post_init__(self) -> None:
        if self.coro is None:
            async def wrapper() -> list[T]:
                return []

            self.coro = wrapper

    def append(self, item: T) -> None:
        # any interaction, load elems
        self.list_.append(item)

    def insert(self, index: int, item: T) -> None:
        # load elems
        self.list_.insert(index, item)

    def clear(self) -> None:
        # load elems
        self.list_.clear()

    def extend(self, data: list) -> None:
        # load elems
        self.list_.extend(data)

    def __repr__(self) -> str:
        # load elems
        return f'{self.list_!r}'

    def __str__(self) -> str:
        # load elems
        return repr(self)

    def __eq__(self, other: Any) -> bool:
        # load elems
        if isinstance(other, _AsyncList):
            return self.list_ == other.list_
        return False

    def __iter__(self):
        # load elems
        yield from self.list_

    @property
    async def as_async(self):
        res = await self.coro()
        self.list_ += res
        return res


alist: TypeAlias = _AsyncList
