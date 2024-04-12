from collections.abc import Callable, Coroutine
from typing import TypeVar, Generic, Optional, TypeAlias, Any, Self

T = TypeVar('T')
CoroutineFactory = Callable[[], Coroutine]


class _AsyncList(Generic[T]):
    """
    Example:
        for batch in await product.items.load():
            for item in await batch.items.load():
                print(item)
    """

    def __init__(self, data: CoroutineFactory | list[T] | None = None) -> None:
        if callable(data):
            self._coro = data
        elif isinstance(data, list):
            self._coro = lambda: self._coro_list(data.copy())
        else:
            self._coro = self._coro_list

        self._list: list[T] = []
        self.is_loaded: bool = False

    @staticmethod
    async def _coro_list(data: Optional[list[T]] = None) -> list[T]:
        return data or []

    @staticmethod
    def check_loaded(func: Callable) -> Callable:
        def wrapper(self, *args, **kw) -> Any:
            assert self.is_loaded, (
                "You can do operations when you have already loaded the list"
            )
            return func(self, *args, **kw)
        return wrapper

    @check_loaded
    def append(self, value: T) -> None:
        self._list.append(value)

    def __getitem__(self, key: int) -> T:
        return self._list[key]

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, list):
            return self._list == other
        return False

    def __repr__(self) -> str:
        return f"{self._list}"

    def __str__(self) -> str:
        return repr(self)

    async def load(self) -> Self:
        """
        Idempotently load list from coroutine.
        """
        if not self.is_loaded:
            res = await self._coro()
            self._list = res
            self.is_loaded = True
        return self


alist: TypeAlias = _AsyncList
