import abc
from collections.abc import Iterator
from typing import TypeVar, Generic
from uuid import UUID

from seedwork.domain.entities import Entity
from seedwork.domain.events import Event

T = TypeVar('T', bound=Entity)


class IGenericRepository(Generic[T], metaclass=abc.ABCMeta):
    identity_map: dict[UUID, T]

    @abc.abstractmethod
    async def add(self, entity: T) -> UUID: ...

    @abc.abstractmethod
    async def delete(self, entity: T) -> None: ...

    @abc.abstractmethod
    async def delete_by_id(self, entity_id: UUID) -> None: ...

    @abc.abstractmethod
    async def get_by_id(
        self,
        entity_id: UUID,
        for_update: bool = False
    ) -> T | None:
        ...

    @abc.abstractmethod
    def persist(self, entity: T) -> None: ...

    @abc.abstractmethod
    def persist_all(self) -> None: ...

    @abc.abstractmethod
    def collect_events(self) -> Iterator[Event]: ...

    @abc.abstractmethod
    async def count(self) -> int: ...

    @abc.abstractmethod
    async def list(self) -> list[T]: ...
