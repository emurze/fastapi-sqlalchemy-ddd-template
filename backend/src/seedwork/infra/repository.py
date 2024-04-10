import itertools
from typing import NoReturn

from sqlalchemy import select, func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.domain.entities import Entity
from seedwork.domain.errors import EntityAlreadyExistsError
from seedwork.domain.events import Event
from seedwork.domain.mapper import IDataMapper
from seedwork.domain.repositories import IGenericRepository

from collections.abc import Iterator

from seedwork.infra.database import Model


class SqlAlchemyRepository(IGenericRepository):
    mapper_class: type[IDataMapper]
    model_class: type[Model]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.mapper = self.mapper_class()
        self._identity_map: dict = {}

    async def add(self, entity: Entity) -> NoReturn | int:
        try:
            self._identity_map[entity.id] = entity
            model = await self.mapper.entity_to_model(entity)
            self.session.add(model)
            return entity.id
        except IntegrityError:  # where is IntegrityError ?
            raise EntityAlreadyExistsError()

    async def delete(self, entity: Entity) -> None:
        model = await self.session.get(self.model_class, entity.id)
        await self.session.delete(model)

    async def delete_by_id(self, entity_id: int) -> None:
        model = await self.session.get(self.model_class, entity_id)
        await self.session.delete(model)

    async def get_by_id(
        self,
        entity_id: int,
        for_update: bool = False,
    ) -> Entity | None:
        model = await self.session.get(
            self.model_class, entity_id, with_for_update=for_update
        )

        if model is None:
            return None

        entity = await self.mapper.model_to_entity(model)

        # Saves store_entity events
        if store_entity := self._identity_map.get(entity.id):
            return store_entity

        self._identity_map[entity.id] = entity
        return entity

    def collect_events(self) -> Iterator[Event]:
        return itertools.chain.from_iterable(
            entity.collect_events() for entity in self._identity_map.values()
        )

    # persist
    # TypeVar("T")

    # Query
    async def count(self) -> int:
        query = select(func.Count(self.model_class))
        res = await self.session.execute(query)
        return res.scalar_one()

    async def list(self) -> list[Entity]:
        query = select(self.model_class)
        res = await self.session.execute(query)
        return [*res.scalars()]


class InMemoryRepository(IGenericRepository):
    mapper_class: type[IDataMapper]

    def __init__(self) -> None:
        self.mapper = self.mapper_class()
        self._objects: dict[int, Entity] = {}

    async def add(self, entity: Entity) -> int:
        self._objects[entity.id] = entity
        return entity.id

    async def delete(self, entity: Entity) -> None:
        del self._objects[entity.id]

    async def delete_by_id(self, entity_id: int) -> None:
        del self._objects[entity_id]

    async def get_by_id(
        self,
        entity_id: int,
        for_update: bool = False,
    ) -> Entity | None:
        try:
            return next(
                model
                for model in self._objects.values()
                if model.id == entity_id
            )
        except StopIteration:
            return None

    async def count(self) -> int:
        return len(self._objects)

    async def list(self) -> list[Entity]:
        return list(self._objects.values())

    def collect_events(self) -> Iterator[Event]:
        return itertools.chain.from_iterable(
            entity.collect_events() for entity in self._objects.values()
        )
