import itertools
from typing import NoReturn, Any
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.domain.entities import Entity
from seedwork.domain.events import Event
from seedwork.domain.mappers import IDataMapper
from seedwork.domain.repositories import IGenericRepository

from collections.abc import Iterator


class Deleted:
    def __repr__(self) -> str:
        return "<Deleted entity>"

    def __str__(self) -> str:
        return "<Deleted entity>"


DELETED = Deleted()  # Why can't we just delete them


class SqlAlchemyRepository(IGenericRepository):
    mapper_class: type[IDataMapper]
    model_class: type[Any]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.mapper = self.mapper_class()
        self.identity_map: dict[UUID, Any] = {}

    def _check_not_deleted(self, entity_id: UUID) -> NoReturn | None:
        assert (
            self.identity_map.get(entity_id) is not DELETED
        ), f"Entity {entity_id} already deleted"
        return None

    async def add(self, entity: Entity) -> UUID:
        self.identity_map[entity.id] = entity
        model = self.mapper.entity_to_model(entity)
        self.session.add(model)
        return entity.id

    async def delete(self, entity: Entity) -> None:
        self._check_not_deleted(entity.id)
        self.identity_map[entity.id] = DELETED
        if model := await self.session.get(self.model_class, entity.id):
            await self.session.delete(model)

    async def delete_by_id(self, entity_id: UUID) -> None:
        self._check_not_deleted(entity_id)
        self.identity_map[entity_id] = DELETED
        if model := await self.session.get(self.model_class, entity_id):
            await self.session.delete(model)

    async def get_by_id(
        self,
        entity_id: UUID,
        for_update: bool = False,
    ) -> Entity | None:
        model = await self.session.get(
            self.model_class, entity_id, with_for_update=for_update
        )

        if model is None:
            return None

        entity = self.mapper.model_to_entity(model)

        # Saves events stored in entity
        if store_entity := self.identity_map.get(entity.id):
            return store_entity

        self.identity_map[entity.id] = entity
        return entity

    def persist(self, entity: Entity) -> None:
        """
        Persists all the changes made to the entity.
        Basically, entity is mapped to a model instance using a data mapper,
        and then added to sqlalchemy session.
        """
        self._check_not_deleted(entity.id)
        assert entity.id in self.identity_map, (
            "Cannon persist entity which is unknown to the repo. "
            "Did you forget to call repo.add() for this entity?"
        )
        instance = self.mapper.entity_to_model(entity)
        merged = self.session.merge(instance)
        self.session.add(merged)

    def persist_all(self) -> None:
        """
        Persists all changes made to entities present in the identity map.
        """
        for entity in self.identity_map.values():
            if entity is not DELETED:
                self.persist(entity)

    def collect_events(self) -> Iterator[Event]:
        return itertools.chain.from_iterable(
            entity.collect_events() for entity in self.identity_map.values()
            if entity is not DELETED
        )

    async def count(self) -> int:
        query = select(func.count()).select_from(self.model_class)
        res = await self.session.execute(query)
        return res.scalar_one()

    async def list(self) -> list[Entity]:
        query = select(self.model_class)
        res = await self.session.execute(query)
        return [self.mapper.model_to_entity(model) for model in res.scalars()]


class InMemoryRepository(IGenericRepository):
    def __init__(self) -> None:
        self.identity_map: dict[UUID, Entity] = {}

    async def add(self, entity: Entity) -> UUID:
        self.identity_map[entity.id] = entity
        return entity.id

    async def delete(self, entity: Entity) -> None:
        del self.identity_map[entity.id]

    async def delete_by_id(self, entity_id: UUID) -> None:
        del self.identity_map[entity_id]

    async def get_by_id(
        self,
        entity_id: UUID,
        for_update: bool = False,
    ) -> Entity | None:
        try:
            return next(
                model
                for model in self.identity_map.values()
                if model.id == entity_id
            )
        except StopIteration:
            return None

    async def count(self) -> int:
        return len(self.identity_map)

    async def list(self) -> list[Entity]:
        return list(self.identity_map.values())

    def persist(self, entity: Entity) -> None:
        ...

    def persist_all(self) -> None:
        ...

    def collect_events(self) -> Iterator[Event]:
        return itertools.chain.from_iterable(
            entity.collect_events() for entity in self.identity_map.values()
        )
