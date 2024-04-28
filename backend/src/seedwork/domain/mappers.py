import abc

from typing import TypeVar, Generic, Any
from seedwork.domain import entities as e

Model = TypeVar("Model", bound=Any)
Entity = TypeVar("Entity", bound=e.Entity)


class IDataMapper(abc.ABC, Generic[Entity, Model]):
    def __init__(self, model_class: type) -> None:
        self.model_class = model_class

    @abc.abstractmethod
    def model_to_entity(self, model: Model) -> Entity: ...

    @abc.abstractmethod
    def update_model(self, entity: Entity, model: Model) -> None: ...

    def entity_to_model(self, entity: Entity) -> Model:
        model = self.model_class()
        self.update_model(entity, model)
        return model
