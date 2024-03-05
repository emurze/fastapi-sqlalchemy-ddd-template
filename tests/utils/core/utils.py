from shared.infra.sqlalchemy_orm.base import base
from shared.infra.sqlalchemy_orm.common import suppress_echo
from tests.utils.db import async_engine


async def restart_tables() -> None:
    """
    Cleans tables data before run test function
    """

    async with async_engine.begin() as conn:
        async with suppress_echo(async_engine):
            await conn.run_sync(base.metadata.drop_all)
            await conn.run_sync(base.metadata.create_all)
        await conn.commit()


async def echo_restart_tables() -> None:
    """
    Cleans tables data before run test function
    """

    async with async_engine.begin() as conn:
        async with suppress_echo(async_engine):
            await conn.run_sync(base.metadata.drop_all)

        await conn.run_sync(base.metadata.create_all)
        await conn.commit()
