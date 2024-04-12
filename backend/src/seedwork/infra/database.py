from collections.abc import AsyncGenerator, Iterator
from contextlib import asynccontextmanager

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import DeclarativeBase

from seedwork.utils.functional import mixin_for


class ModelBase(mixin_for(DeclarativeBase)):  # type: ignore
    @classmethod
    def get_fields(cls) -> Iterator[str]:
        return (field.name for field in inspect(cls).c)

    def as_dict(self) -> dict:
        return {key: getattr(self, key) for key in self.get_fields()}

    def __repr__(self) -> str:
        cls = type(self)
        kwargs = ', '.join(
            f'{col.name}={getattr(self, col.name)!r}'
            for col in inspect(cls).c
        )
        return f"{cls.__name__}({kwargs})"


@asynccontextmanager
async def suppress_echo(engine: AsyncEngine) -> AsyncGenerator:
    engine.echo = False
    yield
    engine.echo = True
