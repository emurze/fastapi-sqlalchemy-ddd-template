from collections.abc import Callable, Coroutine
from typing import TypeVar, Generic, TypeAlias, Any, Self, Iterator

from seedwork.domain.entities import Entity
from seedwork.domain.value_objects import ValueObject

T = TypeVar('T', bound=Entity | ValueObject)
CoroutineFactory = Callable[[], Coroutine]


class _AsyncList(Generic[T]):
    """
    Usage:
        for batch in await product.items.load():
            for item in await batch.items.load():
                print(item)
    """

    def __init__(
        self,
        sync_list: list[T] | None = None,
        coro_factory: CoroutineFactory | None = None,
    ) -> None:
        assert not (sync_list and coro_factory), (
            "You should pass a sync_list or a coro_factory or None"
        )

        self._coro_factory = coro_factory
        self._sync_list = sync_list.copy() if sync_list else []
        self._data: list[T] = []
        self._is_loaded: bool = False

    async def _get_result(self) -> list[T]:
        if self._coro_factory:
            return await self._coro_factory()
        else:
            return self._sync_list

    def _load_result(self, res: list[T]) -> None:
        if not self._is_loaded:
            self._data = res
            self._is_loaded = True

    async def load(self) -> Self:
        """
        Idempotently load list from coroutine.
        """
        self._load_result(await self._get_result())
        return self

    def load_entity_list(self) -> Self:
        if self._sync_list:
            self._load_result(self._sync_list)
        return self

    def is_loaded(self) -> bool:
        return self._is_loaded

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
        self._data.append(value)

    @check_loaded
    def __getitem__(self, key: int) -> T:
        return self._data[key]

    @check_loaded
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, list):
            return self._data == other
        return False

    @check_loaded
    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def __repr__(self) -> str:
        if self._is_loaded:
            return f"{self._data}"
        else:
            return f"alist(<<lazy>>)"

    def __str__(self) -> str:
        return repr(self)


alist: TypeAlias = _AsyncList
