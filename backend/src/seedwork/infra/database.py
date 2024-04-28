from collections.abc import AsyncGenerator, Iterator, Callable
from contextlib import asynccontextmanager
from typing import Any

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine

from seedwork.domain.structs import alist
from seedwork.utils.functional import get_single_param


class ModelBase:
    awaitable_attrs: Any

    @classmethod
    def get_fields(cls) -> Iterator[str]:
        return (field.name for field in sa.inspect(cls).c)  # type: ignore

    def as_dict(self) -> dict:
        return {key: getattr(self, key) for key in self.get_fields()}

    def update(self, **kw) -> None:
        for key, value in kw.items():
            setattr(self, key, value)

    def as_alist(self, map_items: Callable) -> dict:
        relation_name = get_single_param(map_items)

        async def mapper():
            awaitable = getattr(self.awaitable_attrs, relation_name)
            return map_items(await awaitable)

        return {
            relation_name: alist(
                coro_factory=mapper,
                coro_struct=lambda: getattr(self, relation_name),
            )
        }

    def __repr__(self) -> str:
        column_data = ", ".join(
            f"{col.name}={getattr(self, col.name)}"
            for col in self.__table__.columns  # type: ignore
        )
        rels_data = ", ".join(
            f"{key}={getattr(self, key)}"
            for key in self.__mapper__.relationships.keys()  # type: ignore
        )
        rels_data = ", " + rels_data if rels_data else ""
        return f"{type(self).__name__}({column_data}{rels_data})"


@asynccontextmanager
async def suppress_echo(engine: AsyncEngine) -> AsyncGenerator:
    engine.echo = False
    yield
    engine.echo = True
