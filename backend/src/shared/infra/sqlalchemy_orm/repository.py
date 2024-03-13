from typing import NoReturn

from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from shared.domain.entities import AggregateRoot, EntityId
from shared.domain.exceptions import ResourceNotFoundException
from shared.domain.repositories import IGenericRepository


class SqlAlchemyRepository(IGenericRepository):
    aggregate_root: type[AggregateRoot]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @property
    def model(self) -> type[AggregateRoot]:
        return self.aggregate_root

    async def add(self, entity: AggregateRoot) -> EntityId:
        stmt = (
            insert(self.model)
            .values(**entity.to_dict())
            .returning(self.model.id)
        )
        result_id = await self.session.execute(stmt)
        return result_id.scalar_one()

    async def delete(self, entity_id: EntityId) -> None:
        query = delete(self.model).filter_by(id=entity_id)
        await self.session.execute(query)

    async def get(self, **kw) -> NoReturn | AggregateRoot:
        query = select(self.model).filter_by(**kw)
        res = await self.session.execute(query)
        model = res.scalars().first()

        if model is None:
            raise ResourceNotFoundException()

        return model

    async def get_for_update(self, **kw) -> NoReturn | AggregateRoot:
        query = select(self.model).filter_by(**kw).with_for_update()
        res = await self.session.execute(query)
        model = res.scalars().first()

        if model is None:
            raise ResourceNotFoundException()

        return model

    async def list(self) -> list[AggregateRoot]:
        query = select(self.model)
        posts = await self.session.execute(query)
        return list(posts.scalars().all())
