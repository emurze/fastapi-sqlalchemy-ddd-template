import itertools
from functools import partial, cached_property

from typing import NoReturn, Any, Any as Model, Protocol
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.domain.entities import Entity
from seedwork.domain.events import DomainEvent
from seedwork.domain.mappers import IDataMapper

from collections.abc import Iterator, Callable

from seedwork.domain.repositories import ICommandRepository, IQueryRepository


class Deleted:
    def __repr__(self) -> str:
        return "<Deleted>"

    def __str__(self) -> str:
        return "<Deleted>"


DELETED = Deleted()


class SqlAlchemyCommandRepository(ICommandRepository):
    mapper_class: type[IDataMapper]
    model_class: type[Any]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.mapper = self.mapper_class(self.model_class)
        self.identity_map: dict[UUID, Any] = {}

    def _check_not_deleted(self, entity_id: UUID) -> NoReturn | None:
        """Checks if the entity is deleted."""
        if entity := self.identity_map.get(entity_id):
            assert (
                entity != DELETED
            ), f"Entity {entity_id} has already been deleted."

    def add(self, entity: Entity) -> UUID:
        """
        Marks the entity as added to be added right before commit
        and stores the entity in the identity map for pre-commit logic.
        """
        model = self.mapper.entity_to_model(entity)
        entity.extra["model"] = model
        entity.extra["is_added"] = True
        self.identity_map[entity.id] = entity
        return entity.id

    @cached_property
    def added(self) -> list[Entity]:
        """Retrieves all entities added to this repository."""
        return [
            entity
            for entity in self.identity_map.values()
            if entity.extra.get("is_added")
        ]

    @staticmethod
    def is_added(entity: Entity) -> bool:
        """Checks if the entity is added to this repository."""
        return entity.extra.get("is_added")

    async def delete(self, entity: Entity) -> None:
        """Deletes an entity from the repository and the database."""
        self._check_not_deleted(entity.id)
        self.identity_map[entity.id] = DELETED
        if model := await self.session.get(self.model_class, entity.id):
            await self.session.delete(model)

    async def delete_by_id(self, entity_id: UUID) -> None:
        """Deletes an entity by ID from the repository and the database."""
        self._check_not_deleted(entity_id)
        self.identity_map[entity_id] = DELETED
        if model := await self.session.get(self.model_class, entity_id):
            await self.session.delete(model)

    async def get_by_id(
        self,
        entity_id: UUID,
        for_update: bool = False,
    ) -> Entity | None:
        """
        Retrieves an entity by ID from the repository or the database,
        storing events.
        """
        if stored_entity := self.identity_map.get(entity_id):
            return None if stored_entity is DELETED else stored_entity

        model = await self.session.get(
            self.model_class, entity_id, with_for_update=for_update
        )

        if model is None:
            return None

        entity = self.mapper.model_to_entity(model)
        entity.extra["model"] = model
        self.identity_map[entity.id] = entity
        return entity

    def persist(self, entity: Entity) -> None:
        """Persists all the changes made to the entity."""
        self._check_not_deleted(entity.id)
        assert entity.id in self.identity_map, (
            "Cannot persist entity which is unknown to the repo. "
            "Did you forget to call repo.add() for this entity?"
        )
        self.mapper.update_model(entity, entity.extra["model"])

    def persist_all(self) -> None:
        """
        Persists changes made to entities in the identity map
        and adds entities marked as added to the session.
        """
        for entity in self.identity_map.values():
            if entity is DELETED:
                continue

            self.persist(entity)
            if self.is_added(entity):
                self.session.add(entity.extra["model"])

    def collect_events(self) -> Iterator[DomainEvent]:
        """Collects events from all entities present in the identity map."""
        return itertools.chain.from_iterable(
            entity.collect_events()
            for entity in self.identity_map.values()
            if entity is not DELETED
        )

    async def count(self) -> int:
        """Counts all entities in this repository and from the database."""
        query = select(func.count()).select_from(self.model_class)
        res = await self.session.execute(query)
        return len(self.added) + res.scalar_one()


class InMemoryCommandRepository(ICommandRepository):
    def __init__(self) -> None:
        self.identity_map: dict[UUID, Entity] = {}

    def add(self, entity: Entity) -> UUID:
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
        return len(self.identity_map.values())

    def persist(self, entity: Entity) -> None: ...

    def persist_all(self) -> None: ...

    def collect_events(self) -> Iterator[DomainEvent]:
        return itertools.chain.from_iterable(
            entity.collect_events() for entity in self.identity_map.values()
        )


class SqlAlchemyQueryRepository(IQueryRepository):
    model_class: type[Any]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @staticmethod
    def extend_get_query(query):
        return query

    @staticmethod
    def extend_list_query(query):
        return query

    async def get(self, **kw) -> Model | None:
        query = select(self.model_class).filter_by(**kw)
        query = self.extend_get_query(query)
        res = await self.session.execute(query)
        return res.scalar_one()

    async def list(self) -> list[Model]:
        query = select(self.model_class)
        query = self.extend_list_query(query)
        res = await self.session.execute(query)
        return list(res.scalars())


class _Container(Protocol):
    mapper_class: type[IDataMapper]
    model_class: type[Any]


class InMemoryQueryRepository(IQueryRepository):
    def __init__(self, attr_container: _Container, identity_map: dict) -> None:
        self.identity_map = identity_map
        self.mapper = attr_container.mapper_class(attr_container.model_class)

    async def get(self, **kw) -> Model | None:
        try:
            entity = next(
                model
                for model in self.identity_map.values()
                if model.id == kw.get("id")
            )
            return self.mapper.entity_to_model(entity)
        except StopIteration:
            return None

    async def list(self) -> list[Model]:
        return list(self.identity_map.values())


def as_mem_query(container: _Container) -> Callable:
    return partial(InMemoryQueryRepository, container)
