from collections.abc import Callable, Coroutine
from typing import TypeVar, Generic, Optional, TypeAlias, Any, Self, Iterator
from uuid import UUID

from seedwork.domain.entities import Entity
from seedwork.domain.value_objects import ValueObject

T = TypeVar('T', bound=Entity | ValueObject)
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
            print('CALLABLE')
            self._coro = data
            self._is_data_list = False
        elif isinstance(data, list):
            self._coro = lambda: self._coro_list(data.copy())
            self._data = data.copy()
            self._is_data_list = True
        else:
            self._coro = self._coro_list
            self._is_data_list = False

        self._list: list[T] = []
        self._is_loaded: bool = False

    @staticmethod
    async def _coro_list(data: Optional[list[T]] = None) -> list[T]:
        return data or []

    @staticmethod
    def check_loaded(func: Callable) -> Callable:
        def wrapper(self, *args, **kw) -> Any:
            assert self._is_loaded, (
                "You can make operations when you have already loaded the list"
            )
            return func(self, *args, **kw)
        return wrapper

    @check_loaded
    def append(self, value: T) -> None:
        self._list.append(value)

    @check_loaded
    def __getitem__(self, key: int) -> T:
        return self._list[key]

    @check_loaded
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, list):
            return self._list == other
        return False

    @check_loaded
    def __iter__(self) -> Iterator[T]:
        return iter(self._list)

    def __repr__(self) -> str:
        if self._is_loaded:
            return f"{self._list}"
        else:
            return f"alist(<<lazy>>)"

    def __str__(self) -> str:
        return repr(self)

    def map_relation(self, callback: Callable) -> None:
        if not self.is_loaded() and self._is_data_list:
            self._list = self._data
            self._is_loaded = True

        if self.is_loaded():
            callback(self)

    async def load(self) -> Self:
        """
        Idempotently load list from coroutine.
        """
        if not self._is_loaded:
            res = await self._coro()
            self._list = res
            self._is_loaded = True
        return self

    def is_loaded(self):
        return self._is_loaded


def map_coro(entity_cls: type, coro_factory: CoroutineFactory):
    async def post_list():
        return [entity_cls(**x.as_dict()) for x in await coro_factory()]

    return post_list


alist: TypeAlias = _AsyncList
