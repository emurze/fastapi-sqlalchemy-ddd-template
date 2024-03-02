from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from shared.infra.sqlalchemy_orm.base import base
from shared.infra.sqlalchemy_orm.common import suppress_echo
from tests.shared.config import db_config

db_dsn = db_config.get_dsn()
async_engine = create_async_engine(db_dsn, echo=True, poolclass=NullPool)
async_session_factory = async_sessionmaker(
    async_engine, expire_on_commit=False
)


async def restart_tables() -> None:
    """
    Cleans tables data before run test function
    """

    async with async_engine.begin() as conn:
        async with suppress_echo(async_engine):
            await conn.run_sync(base.metadata.drop_all)

        await conn.run_sync(base.metadata.create_all)
        await conn.commit()
