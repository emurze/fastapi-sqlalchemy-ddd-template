from collections.abc import AsyncGenerator, Iterator
from contextlib import asynccontextmanager

from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import DeclarativeBase


class Model(DeclarativeBase):
    __allow_unmapped__ = True
    id: int

    @classmethod
    def get_fields(cls) -> Iterator[str]:
        return (field.name for field in inspect(cls).c)

    def as_dict(self) -> dict:
        return {key: getattr(self, key) for key in self.get_fields()}


@asynccontextmanager
async def suppress_echo(engine: AsyncEngine) -> AsyncGenerator:
    engine.echo = False
    yield
    engine.echo = True
