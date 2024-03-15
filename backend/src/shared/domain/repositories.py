import abc
from typing import List

from shared.domain.entities import AggregateRoot


class IGenericRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def add(self, entity: AggregateRoot) -> int: ...

    @abc.abstractmethod
    async def delete(self, entity: AggregateRoot) -> None: ...

    @abc.abstractmethod
    async def delete_by_id(self, entity_id: int) -> None: ...

    @abc.abstractmethod
    async def get_by_id(
        self, entity_id: int, for_update: bool = False
    ) -> AggregateRoot | None: ...

    @abc.abstractmethod
    async def count(self) -> int: ...

    @abc.abstractmethod
    async def list(self) -> List[AggregateRoot]: ...

    @abc.abstractmethod
    def collect_events(self): ...
