import abc
from typing import List

from shared.domain.entities import EntityId, AggregateRoot


class IGenericRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def add(self, entity: AggregateRoot) -> EntityId: ...

    @abc.abstractmethod
    async def delete(self, entity_id: EntityId) -> None: ...

    @abc.abstractmethod
    async def get(self, **kw) -> AggregateRoot: ...

    @abc.abstractmethod
    async def get_for_update(self, **kw) -> AggregateRoot: ...

    @abc.abstractmethod
    async def list(self) -> List[AggregateRoot]: ...
