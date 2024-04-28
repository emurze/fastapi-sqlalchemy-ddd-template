import enum
from collections.abc import Callable, Coroutine
from typing import TypeVar, Generic, TypeAlias, Any, Self, Iterator

T = TypeVar("T", bound=Any)
R = TypeVar("R", bound=Any)
CoroutineFactory = Callable[[], Coroutine]


class ListAction(enum.Enum):
    EXTEND = enum.auto()
    APPEND = enum.auto()
    SETATTR = enum.auto()
    POP = enum.auto()


class _AsyncList(Generic[T]):
    """
    Usage:
        for batch in await product.items.load():
            for item in await batch.items.load():
                print(item)
    """

    def __init__(
        self,
        sync_list: list[T] | Iterator[T] | None = None,
        coro_factory: CoroutineFactory | None = None,
        coro_struct: Any | None = None,
    ) -> None:
        assert not (
            sync_list and coro_factory
        ), "You should pass a sync_list or a coro_factory or None"
        self._coro_factory = coro_factory
        self._coro_struct: Any = coro_struct

        if not sync_list:
            self._sync_list = []
        elif not isinstance(sync_list, list):
            self._sync_list = list(sync_list)
        else:
            self._sync_list = sync_list.copy()

        self._data: list[T] = []
        self._is_loaded: bool = False
        self._actions: list[tuple[ListAction, Any]] = []

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
        if self.is_entity_list():
            self._load_result(self._sync_list)
        return self

    def is_loaded(self) -> bool:
        return self._is_loaded

    def is_entity_list(self) -> bool:
        return bool(self._sync_list)

    def execute_actions(self, mapper) -> None:
        relation = self._coro_struct()
        for action, params in self._actions:
            match action:
                case ListAction.APPEND:
                    relation.append(mapper(params)[0])
                case ListAction.EXTEND:
                    relation.extend(mapper(params))
                case ListAction.POP:
                    relation.pop(*params)
                case ListAction.SETATTR:
                    relation[params[0]] = mapper([params[1]])[0]

        for model, entity in zip(relation, self._data):  # todo: Why?
            if hasattr(entity, "extra"):
                if actions := entity.extra.get("actions"):
                    for key, value in actions:
                        model.update(**{key: value})

    @staticmethod
    def check_loaded(func: Callable) -> Callable:
        def wrapper(self, *args, **kw) -> Any:
            assert (
                self._is_loaded
            ), "You can make operations when you have already loaded the list"
            return func(self, *args, **kw)

        return wrapper

    @check_loaded
    def append(self, value: T) -> None:
        self._actions.append((ListAction.APPEND, [value]))
        self._data.append(value)

    @check_loaded
    def pop(self, index: int = -1, /) -> T:
        self._actions.append((ListAction.POP, [index]))
        return self._data.pop(index)

    @check_loaded
    def find_one(self, **kw) -> T | None:
        """Finds first accepted item"""

        try:
            return next(
                item
                for key, value in kw.items()
                for item in self._data
                if getattr(item, key) == value
            )
        except StopIteration:
            return None

    @check_loaded
    def __getitem__(self, key: int) -> T:
        return self._data[key]

    @check_loaded
    def __setitem__(self, key, value) -> None:
        self._actions.append((ListAction.SETATTR, [key, value]))
        self._data[key] = value

    @check_loaded
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, list):
            return self._data == other
        return False

    @check_loaded
    def __iter__(self) -> Iterator[T]:
        return iter(self._data)

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        if self._is_loaded:
            return f"{self._data}"
        else:
            return f"alist(<<lazy>>)"

    def __str__(self) -> str:
        return repr(self)


class _AsyncRel(Generic[R]):
    # OneToOne and ManyToMany
    def __init__(
        self,
        sync_val: R | None = None,
        coro_factory: CoroutineFactory | None = None,
        coro_struct: Any | None = None,
    ) -> None:
        assert not (
            sync_val and coro_factory
        ), "You should pass a sync_list or a coro_factory or None"
        self._coro_factory = coro_factory
        self._coro_struct: Any = coro_struct
        self._sync_val = sync_val
        self._data: R | None = None
        self._is_loaded: bool = False

        def __getattr__(self, key: str) -> Any:
            return getattr(self._data, key)

        def __setattr__(self, key: str, value) -> Any:
            return setattr(self._data, key, value)

    @staticmethod
    def check_loaded(func: Callable) -> Callable:
        def wrapper(self, *args, **kw) -> Any:
            assert (
                self._is_loaded
            ), "You can make operations when you have already loaded the item"
            return func(self, *args, **kw)

        return wrapper


alist: TypeAlias = _AsyncList
arel: TypeAlias = _AsyncRel
