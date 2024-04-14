import abc

from typing import Any as Model
from seedwork.domain.entities import Entity


class IDataMapper(abc.ABC):
    @abc.abstractmethod
    def model_to_entity(self, model: Model) -> Entity: ...

    @abc.abstractmethod
    def entity_to_model(self, entity: Entity) -> Model: ...
