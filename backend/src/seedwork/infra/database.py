from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    __allow_unmapped__ = True


@asynccontextmanager
async def suppress_echo(engine: AsyncEngine) -> AsyncGenerator:
    engine.echo = False
    yield
    engine.echo = True
