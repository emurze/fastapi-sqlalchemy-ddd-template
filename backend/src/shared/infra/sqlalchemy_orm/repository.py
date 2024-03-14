from typing import NoReturn, Annotated

from sqlalchemy import select, insert, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from shared.domain.entities import AggregateRoot, EntityId
from shared.domain.exceptions import ResourceNotFoundException
from shared.domain.repositories import IGenericRepository


class SqlAlchemyRepository(IGenericRepository):
    aggregate_root: type[AggregateRoot]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

        assert self.aggregate_root, (
            f"Aggregate root is not set for {type(self)} repository"
        )
        self.model = self.aggregate_root

    async def add(self, entity: AggregateRoot) -> EntityId:
        stmt = (
            insert(self.model)
            .values(**entity.as_dict())
            .returning(self.model.id)
        )
        result_id = await self.session.execute(stmt)
        return result_id.scalar_one()

    async def remove(self, entity: AggregateRoot) -> None:
        await self.session.delete(entity)

    async def remove_by_id(self, entity_id: EntityId) -> None:
        query = delete(self.model).filter_by(id=entity_id)
        await self.session.execute(query)

    async def get_by_id(
        self,
        entity_id: EntityId,
        for_update: Annotated[
            bool,
            "Use it when you want to update retrieved entity."
            "Lock to solve lost update problem"
        ] = False
    ) -> NoReturn | AggregateRoot:
        query = select(self.model).filter_by(id=entity_id)

        if for_update:
            query = query.with_for_update()

        res = await self.session.execute(query)
        model = res.scalars().first()

        if model is None:
            raise ResourceNotFoundException()

        return model

    async def count(self) -> int:
        query = select(func.Count(self.model))
        res = await self.session.execute(query)
        return res.scalar_one()

    async def list(self) -> list[AggregateRoot]:
        query = select(self.model)
        posts = await self.session.execute(query)
        return list(posts.scalars().all())
