import abc

from typing import Any as Model
from seedwork.domain.entities import Entity


class IDataMapper(abc.ABC):
    entity_class: type[Entity]
    model_class: type[Model]

    @abc.abstractmethod
    def entity_to_model(self, entity: Entity) -> Model: ...

    @abc.abstractmethod
    def model_to_entity(self, model: Model) -> Entity: ...
