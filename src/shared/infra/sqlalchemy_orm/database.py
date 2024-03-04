from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from shared.infra.sqlalchemy_orm.config import db_config

async_engine = create_async_engine(db_config.get_dsn(), echo=True)
async_session_factory = async_sessionmaker(async_engine)


def get_session_factory():
    return async_session_factory


async def get_session() -> AsyncIterator[AsyncSession]:
    async with async_session_factory() as session:
        yield session
