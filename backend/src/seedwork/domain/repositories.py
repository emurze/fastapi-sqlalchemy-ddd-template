import abc
from typing import List

from seedwork.domain.entities import Entity


class IGenericRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def add(self, entity: Entity) -> int: ...

    @abc.abstractmethod
    async def delete(self, entity: Entity) -> None: ...

    @abc.abstractmethod
    async def delete_by_id(self, entity_id: int) -> None: ...

    @abc.abstractmethod
    async def get_by_id(
        self,
        entity_id: int,
        for_share: bool = False,
        for_update: bool = False,
    ) -> Entity | None: ...

    @abc.abstractmethod
    async def count(self) -> int: ...

    @abc.abstractmethod
    async def list(self) -> List[Entity]: ...

    @abc.abstractmethod
    async def persist(self, entity: Entity) -> None: ...

    @abc.abstractmethod
    async def persist_all(self) -> None: ...

    @abc.abstractmethod
    def collect_events(self): ...
