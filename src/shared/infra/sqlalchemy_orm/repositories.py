from typing import NoReturn, Any as Model, List

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from shared.domain.repository import IGenericRepository


class SqlAlchemyRepository(IGenericRepository):
    model: type[Model]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, **kw) -> Model:
        stmt = (
            insert(self.model)
            .values(**kw)
            .returning(self.model)
        )
        model = await self.session.execute(stmt)
        return model.scalar_one()

    async def get(self, **kw) -> Model:
        query = select(self.model).filter_by(**kw)
        res = await self.session.execute(query)
        model = res.scalars().first()
        return model

    async def get_for_update(self, **kw) -> Model:
        query = select(self.model).filter_by(**kw).with_for_update()
        res = await self.session.execute(query)
        model = res.scalars().first()
        return model

    async def list(self) -> NoReturn | list[Model]:
        query = select(self.model)
        posts = await self.session.execute(query)
        return list(posts.scalars().all())

    async def delete_one(self, **kw) -> Model:
        id_value = kw.get('id')
        assert len(kw) == 1 and id_value is not None, \
            "delete_one accepts only one id parameter"

        query = delete(self.model).filter_by(id=id_value).returning(self.model)
        model = await self.session.execute(query)
        return model.scalar_one()

    async def delete(self, **kw) -> List[Model]:
        query = delete(self.model).filter_by(**kw).returning(self.model)
        model = await self.session.execute(query)
        return list(model.scalars().all())
