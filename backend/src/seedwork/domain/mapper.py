import abc

from typing import Any as Model
from seedwork.domain.entities import Entity


class IDataMapper(abc.ABC):
    @abc.abstractmethod
    async def entity_to_model(self, entity: Entity) -> Model: ...

    @abc.abstractmethod
    async def model_to_entity(self, model: Model) -> Entity: ...
