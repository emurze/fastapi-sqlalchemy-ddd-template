from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncEngine


@asynccontextmanager
async def suppress_echo(engine: AsyncEngine) -> AsyncGenerator:
    engine.echo = False
    yield
    engine.echo = True
