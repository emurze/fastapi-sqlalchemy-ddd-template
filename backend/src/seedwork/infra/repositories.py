import itertools
from functools import partial

from typing import Any, Optional
from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.domain.entities import AggregateRoot
from seedwork.domain.events import DomainEvent
from seedwork.domain.repositories import IGenericRepository

from collections.abc import Iterator, Callable

from seedwork.infra.awaitable_attrs import (
    SqlAlchemyAwaitableAttrs,
    MemoryAwaitableAttrs,
    getattr_with_loading_errors,
)


class Deleted:
    def __repr__(self) -> str:
        return "<Deleted>"


DELETED = Deleted()


class SqlAlchemyRepository(IGenericRepository):
    entity_class: type[Any]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.identity_map: dict[UUID, Any] = {}

    def add(self, entity: AggregateRoot) -> UUID:
        self.session.add(entity)
        self.identity_map[entity.id] = entity
        return entity.id

    async def delete(self, entity: AggregateRoot) -> None:
        await self.delete_by_id(entity.id)

    async def delete_by_id(self, entity_id: UUID) -> None:
        assert (
            self.identity_map.get(entity_id) != DELETED
        ), f"Entity {entity_id} has already been deleted."

        self.identity_map[entity_id] = DELETED
        if model := await self.session.get(self.entity_class, entity_id):
            await self.session.delete(model)

    async def get_by_id(
        self,
        entity_id: UUID,
        for_update: bool = False,
    ) -> AggregateRoot | None:
        """
        Retrieves an entity by ID from the repository.
        Sets SQLAlchemy awaitable for lazy loading.
        """

        if stored_entity := self.identity_map.get(entity_id):
            return None if stored_entity is DELETED else stored_entity

        entity: Any = await self.session.get(
            self.entity_class, entity_id, with_for_update=for_update
        )
        if entity:
            entity.awaitable_attrs = SqlAlchemyAwaitableAttrs.make(entity)
            self.identity_map[entity.id] = entity

        return entity

    async def count(self) -> int:
        query = select(func.count()).select_from(self.entity_class)
        return (await self.session.execute(query)).scalar_one()

    def collect_events(self) -> Iterator[DomainEvent]:
        return itertools.chain.from_iterable(
            entity.collect_events()
            for entity in self.identity_map.values()
            if entity is not DELETED
        )


class InMemoryRepository(IGenericRepository):
    """
    Should always be wrapped by `bind_getter` and `clear_getter` methods.  # Todo: should be wrapped, one example
    These methods set loading errors.  # todo: normal view
    """

    def __init__(self, entity_class) -> None:
        self.entity_class = entity_class
        self.identity_map: dict[UUID, AggregateRoot] = {}
        self._old_entity_getter: Optional[Callable] = None

    def add(self, entity: AggregateRoot) -> UUID:
        self.identity_map[entity.id] = entity
        return entity.id

    async def delete(self, entity: AggregateRoot) -> None:
        del self.identity_map[entity.id]

    async def delete_by_id(self, entity_id: UUID) -> None:
        del self.identity_map[entity_id]

    async def count(self) -> int:
        return len(self.identity_map.values())

    def collect_events(self) -> Iterator[DomainEvent]:
        return itertools.chain.from_iterable(
            entity.collect_events() for entity in self.identity_map.values()
        )

    async def get_by_id(
        self,
        entity_id: UUID,
        for_update: bool = False,
    ) -> AggregateRoot | None:
        """
        Retrieves an entity by ID from the repository.
        Sets memory awaitable for lazy loading.
        """
        if entity := self.identity_map.get(entity_id):
            entity.awaitable_attrs = MemoryAwaitableAttrs.make(entity)
        return entity

    def bind_getter(self) -> None:  # todo: only for me, test with explicit binding
        """Binds getter with loading errors to the entity_class."""
        self._old_entity_getter = self.entity_class.__getattribute__
        self.entity_class.__getattribute__ = getattr_with_loading_errors

    def clear_getter(self) -> None:
        """Clears the getter with loading errors from the entity_class."""
        self.entity_class.__getattribute__ = self._old_entity_getter
        self._clear_flags()

    def _clear_flags(self) -> None:
        """Clears flags set by awaitable attrs for the custom getter."""
        for item in self.identity_map.values():
            if attrs := getattr(item.awaitable_attrs, "_awaitable_attrs"):
                getattr(attrs, "_clear_flags")()


def as_memory(sql_repo: type[SqlAlchemyRepository]) -> Callable:
    """Decorator to convert a SQLAlchemy repository to an in-memory version."""
    return partial(InMemoryRepository, sql_repo.entity_class)
