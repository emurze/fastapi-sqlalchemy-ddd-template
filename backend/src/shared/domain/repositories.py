import abc
from typing import List, NoReturn

from shared.domain.entities import EntityId, AggregateRoot


class IGenericRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def add(self, entity: AggregateRoot) -> EntityId: ...

    @abc.abstractmethod
    async def remove(self, entity: AggregateRoot) -> None: ...

    @abc.abstractmethod
    async def remove_by_id(self, entity_id: EntityId) -> None: ...

    @abc.abstractmethod
    async def get_by_id(
        self, entity_id: EntityId, for_update: bool = False
    ) -> NoReturn | AggregateRoot:
        ...

    @abc.abstractmethod
    async def count(self) -> int: ...

    @abc.abstractmethod
    async def list(self) -> List[AggregateRoot]: ...
