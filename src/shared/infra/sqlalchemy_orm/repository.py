from typing import NoReturn, Any as Model, List

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from shared.domain.exceptions import ResourceNotFoundError
from shared.domain.repository import IGenericRepository


class SqlAlchemyRepository(IGenericRepository):
    model: type[Model]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, **kw) -> None:
        stmt = insert(self.model).values(**kw)
        await self.session.execute(stmt)

    async def delete(self, **kw) -> None:
        query = delete(self.model).filter_by(**kw)
        await self.session.execute(query)

    async def get(self, **kw) -> NoReturn | Model:
        query = select(self.model).filter_by(**kw)
        res = await self.session.execute(query)
        model = res.scalars().first()

        if model is None:
            raise ResourceNotFoundError()

        return model

    async def get_for_update(self, **kw) -> NoReturn | Model:
        query = select(self.model).filter_by(**kw).with_for_update()
        res = await self.session.execute(query)
        model = res.scalars().first()

        if model is None:
            raise ResourceNotFoundError()

        return model

    async def list(self) -> list[Model]:
        query = select(self.model)
        posts = await self.session.execute(query)
        return list(posts.scalars().all())
