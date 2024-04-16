import inspect
from collections.abc import AsyncGenerator, Iterator, Callable
from contextlib import asynccontextmanager

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine

from seedwork.domain.async_structs import alist


class LazyAsyncAttrsMixin:
    @staticmethod
    def _get_mapper_param(mapper: Callable) -> str:
        res = inspect.signature(mapper)
        params = tuple(res.parameters)
        assert len(params) == 1, "Map callback should have only one parameter."
        return params[0]

    def as_alist(self, map_items: Callable) -> dict:
        rel_name = self._get_mapper_param(map_items)

        async def mapper():
            awaitable = getattr(self.awaitable_attrs, rel_name)  # type: ignore
            return map_items(await awaitable)

        return {rel_name: alist(coro_factory=mapper)}


class ModelBase(LazyAsyncAttrsMixin):
    @classmethod
    def get_fields(cls) -> Iterator[str]:
        return (field.name for field in sa.inspect(cls).c)  # type: ignore

    def as_dict(self) -> dict:
        return {key: getattr(self, key) for key in self.get_fields()}

    def update(self, **kw) -> None:
        for key, value in kw.items():
            setattr(self, key, value)

    def __repr__(self) -> str:
        cls = type(self)
        kwargs = ', '.join(
            f'{col.name}={getattr(self, col.name)!r}'
            for col in sa.inspect(cls).c  # type: ignore
        )
        return f"{cls.__name__}({kwargs})"


@asynccontextmanager
async def suppress_echo(engine: AsyncEngine) -> AsyncGenerator:
    engine.echo = False
    yield
    engine.echo = True
