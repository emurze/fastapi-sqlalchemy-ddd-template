import abc

from typing import TypeVar, Generic, Any
from seedwork.domain import entities as e

Model = TypeVar('Model', bound=Any)
Entity = TypeVar('Entity', bound=e.Entity)


class IDataMapper(abc.ABC, Generic[Entity, Model]):
    @abc.abstractmethod
    def model_to_entity(self, model: Model) -> Entity: ...

    @abc.abstractmethod
    def update_model(self, entity: Entity, model: Model) -> Model: ...
