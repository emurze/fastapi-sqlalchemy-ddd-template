import abc
from uuid import UUID

from seedwork.domain.entities import Entity


class IGenericRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def add(self, entity: Entity) -> UUID: ...

    @abc.abstractmethod
    async def delete(self, entity: Entity) -> None: ...

    @abc.abstractmethod
    async def delete_by_id(self, entity_id: UUID) -> None: ...

    @abc.abstractmethod
    async def get_by_id(
        self,
        entity_id: UUID,
        for_update: bool = False,
    ) -> Entity | None: ...

    @abc.abstractmethod
    async def count(self) -> int: ...

    @abc.abstractmethod
    async def list(self) -> list[Entity]: ...

    # PERSIST

    @abc.abstractmethod
    def collect_events(self): ...
