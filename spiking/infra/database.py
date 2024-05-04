from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import registry

from seedwork.infra.database import suppress_echo

mapped_registry = registry()


async def restart_db(engine: AsyncEngine) -> None:
    async with engine.begin() as conn:
        with suppress_echo(engine):
            await conn.run_sync(mapped_registry.metadata.drop_all)
            await conn.run_sync(mapped_registry.metadata.create_all)
        await conn.commit()
