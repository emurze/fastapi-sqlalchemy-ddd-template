import contextlib
import itertools
from functools import partial

from typing import Any
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
    getattr_with_unloaded_relations_raised,
)


class Deleted:
    def __repr__(self) -> str:
        return "<Deleted>"


DELETED = Deleted()


class SqlAlchemyRepository(IGenericRepository[AggregateRoot]):
    entity_class: type[AggregateRoot]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.identity_map: dict[UUID, Any] = {}

    def add(self, entity: AggregateRoot) -> UUID:
        self.session.add(entity)
        self.identity_map[entity.id] = entity
        if not hasattr(entity, "_events"):
            entity._events = []
        if not hasattr(entity, "_awaitable_attrs"):
            entity._awaitable_attrs = SqlAlchemyAwaitableAttrs.make(entity)

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
        Sets memory awaitable_attr for async lazy loading.
        """

        if stored_entity := self.identity_map.get(entity_id):
            return None if stored_entity is DELETED else stored_entity

        entity: Any = await self.session.get(
            self.entity_class, entity_id, with_for_update=for_update
        )
        if entity:
            entity._awaitable_attrs = SqlAlchemyAwaitableAttrs.make(entity)
            entity._events = []
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


class InMemoryRepository(IGenericRepository[AggregateRoot]):
    """
    In-memory repository implementation.

    Should always be wrapped by `override_getter` and `restore_getter` methods.
    Example:
        ```
        repository = InMemoryRepository(Entity)
        with raise_loading_errors(repository):
            # Access entities here
        ```

    These methods enable raising loading errors when accessing
    unloaded lazy attributes and relations.
    """

    def __init__(self, entity_class: type[AggregateRoot]) -> None:
        self.entity_class: type[AggregateRoot] = entity_class
        self.identity_map: dict[UUID, Any] = {}
        self._old_entity_getter: Any = None

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
        Sets memory awaitable_attr for async lazy loading.
        """
        if entity := self.identity_map.get(entity_id):
            entity._awaitable_attrs = MemoryAwaitableAttrs.make(entity)
        return entity

    def override_getter(self) -> None:
        """Overrides entity class __getattribute__."""
        self._old_entity_getter = self.entity_class.__getattribute__
        self.entity_class.__getattribute__ = (
            getattr_with_unloaded_relations_raised
        )

    def restore_getter(self) -> None:
        """Restores entity class __getattribute__ to previous state."""
        self.entity_class.__getattribute__ = self._old_entity_getter
        self._deletes_markers()

    def _deletes_markers(self) -> None:
        """Deletes markers set by awaitable_attrs for the overridden getter."""
        for item in self.identity_map.values():
            if attrs := getattr(item.awaitable_attrs, "_awaitable_attrs"):
                getattr(attrs, "_deletes_markers")()


@contextlib.contextmanager
def raise_unloaded_relations(repository: InMemoryRepository) -> Iterator[None]:
    """
    Wraps your repository to raise errors when accessing unloaded
    lazy attributes and relations outside a unit of work.
    """
    repository.override_getter()
    yield
    repository.restore_getter()


def as_memory(sql_repo: type[SqlAlchemyRepository]) -> Callable:
    """Decorator to convert a SQLAlchemy repository to an in-memory version."""
    return partial(InMemoryRepository, sql_repo.entity_class)
