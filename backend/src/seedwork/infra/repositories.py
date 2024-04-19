import itertools
from typing import NoReturn, Any, Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.domain.entities import Entity
from seedwork.domain.events import DomainEvent
from seedwork.domain.mappers import IDataMapper

from collections.abc import Iterator, Callable

from seedwork.domain.repositories import ICommandRepository, IQueryRepository
from tests.seedwork.confdata.repositories import Model


def default_middleware(query):
    return query


class Deleted:
    def __repr__(self) -> str:
        return "<Deleted entity>"

    def __str__(self) -> str:
        return "<Deleted entity>"


DELETED = Deleted()


class SqlAlchemyCommandRepository(ICommandRepository):
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
        model = self.model_class()
        self.mapper.update_model(entity, model)
        entity.extra_kw["model"] = model
        self.identity_map[entity.id] = entity
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
        if not entity.extra_kw.get("model"):
            entity.extra_kw["model"] = model

        # Saves events stored in entity
        if store_entity := self.identity_map.get(entity.id):
            return store_entity

        self.identity_map[entity.id] = entity
        return entity

    def persist(self, entity: Entity) -> None:
        """Persists all the changes made to the entity."""
        self._check_not_deleted(entity.id)
        assert entity.id in self.identity_map, (
            "Cannot persist entity which is unknown to the repo. "
            "Did you forget to call repo.add() for this entity?"
        )
        self.mapper.update_model(entity, entity.extra_kw["model"])

    def persist_all(self) -> None:
        """Persists changes made to entities present in the identity map."""
        for entity in self.identity_map.values():
            if entity is not DELETED:
                self.persist(entity)

    def collect_events(self) -> Iterator[DomainEvent]:
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


class SqlAlchemyQueryRepository(IQueryRepository):
    model_class: type[Any]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def count(self) -> int:
        query = select(func.count()).select_from(self.model_class)
        res = await self.session.execute(query)
        return res.scalar_one()

    async def get_by_id(
        self,
        model_id: UUID,
        middleware: Optional[Callable] = None,
    ) -> Model:
        middleware = middleware or default_middleware
        query = middleware(select(self.model_class).filter_by(id=model_id))
        res = await self.session.execute(query)
        return res.scalar_one()

    async def list(self, middleware: Optional[Callable] = None) -> list[Model]:
        middleware = middleware or default_middleware
        query = middleware(select(self.model_class))
        res = await self.session.execute(query)
        return list(res.scalars())


class InMemoryCommandRepository(ICommandRepository):
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

    def persist(self, entity: Entity) -> None:
        ...

    def persist_all(self) -> None:
        ...

    def collect_events(self) -> Iterator[DomainEvent]:
        return itertools.chain.from_iterable(
            entity.collect_events() for entity in self.identity_map.values()
        )


class InMemoryQueryRepository(IQueryRepository):
    def __init__(self, identity_map: dict) -> None:
        self.identity_map = identity_map

    async def get_by_id(self, entity_id: UUID) -> Entity | None:
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

    async def list(
        self, middleware: Optional[Callable] = None
    ) -> list[Entity]:
        return list(self.identity_map.values())
