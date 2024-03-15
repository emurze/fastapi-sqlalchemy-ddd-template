from typing import Any, cast

from sqlalchemy import select, insert, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from shared.domain.entities import AggregateRoot
from shared.domain.repositories import IGenericRepository


class SqlAlchemyRepository(IGenericRepository):
    aggregate_root: type[AggregateRoot]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

        assert (
            self.aggregate_root
        ), f"Aggregate root is not set for {type(self)} repository"  # test it
        self.model = cast(Any, self.aggregate_root)

    async def add(self, entity: AggregateRoot) -> int:
        stmt = (
            insert(self.model)
            .values(**entity.as_dict())
            .returning(self.model.id)
        )
        result_id = await self.session.execute(stmt)
        return result_id.scalar_one()

    async def delete(self, entity: AggregateRoot) -> None:
        await self.session.delete(entity)

    async def delete_by_id(self, entity_id: int) -> None:
        query = delete(self.model).filter_by(id=entity_id)
        await self.session.execute(query)

    async def get_by_id(
        self, entity_id: int, for_update: bool = False
    ) -> AggregateRoot | None:
        query = select(self.model).filter_by(id=entity_id)

        if for_update:
            query = query.with_for_update()

        res = await self.session.execute(query)
        return res.scalars().first()

    async def count(self) -> int:
        query = select(func.Count(self.model))
        res = await self.session.execute(query)
        return res.scalar_one()

    async def list(self) -> list[AggregateRoot]:
        query = select(self.model)
        posts = await self.session.execute(query)
        return list(posts.scalars().all())

    def collect_events(self):
        pass
