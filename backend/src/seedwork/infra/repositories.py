from typing import NoReturn

from sqlalchemy import select, insert, delete, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.domain.entities import Entity
from seedwork.domain.errors import EntityAlreadyExistsError
from seedwork.domain.repositories import IGenericRepository

from collections.abc import Callable
from typing import Any, Generator, cast


class SqlAlchemyRepository(IGenericRepository):
    model: type[Entity]
    mapper: type

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add(self, entity: Entity) -> NoReturn | int:
        try:
            stmt = (
                insert(self.model)
                .values(**entity.as_dict())
                .returning(self.model.id)
            )
            result_id = await self.session.execute(stmt)
            return result_id.scalar_one()
        except IntegrityError:
            raise EntityAlreadyExistsError()

    async def delete(self, entity: Entity) -> None:
        await self.session.delete(entity)

    async def delete_by_id(self, entity_id: int) -> None:
        query = delete(self.model).filter_by(id=entity_id)
        await self.session.execute(query)

    async def get_by_id(
        self,
        entity_id: int,
        for_share: bool = False,
        for_update: bool = False,
    ) -> Entity | None:
        query = select(self.model).filter_by(id=entity_id)

        if for_share:
            query = query.with_for_update(key_share=True, read=True)
        elif for_update:
            query = query.with_for_update()

        res = await self.session.execute(query)
        model = res.scalars().first()
        return model if model is None else self.model.model_from(model)

    async def count(self) -> int:
        query = select(func.Count(self.model))
        res = await self.session.execute(query)
        return res.scalar_one()

    async def list(self) -> list[Entity]:   # ??????????
        query = select(self.model)
        posts = await self.session.execute(query)
        return list(posts.scalars().all())

    def persist(self, entity: Entity) -> None:
        pass

    def persist_all(self) -> None:
        pass

    def collect_events(self):
        pass


class GeneratorsManager:
    """
    Imitates database triggers and sequences
    """

    initialized_gens: dict[str, Generator]

    def __init__(self, field_gens: dict[str, Callable]):
        self.initialized_gens = self.initialize_gens(field_gens)

    @staticmethod
    def initialize_gens(field_gens) -> dict[str, Generator]:
        return {field: gen() for field, gen in field_gens.items()}

    def iterate_gens(self, kw: dict) -> dict:
        return kw | {
            field: next(gen)
            for field, gen in self.initialized_gens.items()
            if not kw.get(field)
        }


class InMemoryRepository(IGenericRepository):
    aggregate_root: type[Entity]
    field_gens: dict[str, Callable]

    def __init__(self, gen_manager: type[Any] = GeneratorsManager) -> None:
        self._models: dict[int, Entity] = {}
        self._gen_manager = gen_manager(self.field_gens)
        self.model = cast(Any, self.aggregate_root)

    async def add(self, entity: Entity) -> int:
        kw_gen_values = self._gen_manager.iterate_gens(entity.as_dict())
        extended_instance = self.model(**kw_gen_values)
        self._models[extended_instance.id] = extended_instance
        return extended_instance.id

    async def delete(self, entity: Entity) -> None:
        del self._models[entity.id]

    async def delete_by_id(self, entity_id: int) -> None:
        del self._models[entity_id]

    async def get_by_id(
        self,
        entity_id: int,
        for_share: bool = False,
        for_update: bool = False
    ) -> Entity | None:
        try:
            return next(
                model
                for model in self._models.values()
                if model.id == entity_id
            )
        except StopIteration:
            return None

    async def count(self) -> int:
        return len(self._models)

    async def list(self) -> list[Entity]:
        return list(self._models.values())

    def persist(self, entity: Entity) -> None:
        pass

    def persist_all(self) -> None:
        pass

    def collect_events(self):
        pass
