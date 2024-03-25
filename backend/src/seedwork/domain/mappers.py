import abc
from typing import TypeVar, Generic, Any

from seedwork.domain.entities import Entity

MapperEntity = TypeVar("MapperEntity", bound=Entity)
MapperModel = TypeVar("MapperModel", bound=Any)


class IDataMapper(Generic[MapperEntity, MapperModel], abc.ABC):
    entity: type[MapperEntity]
    model: type[MapperModel]

    @abc.abstractmethod
    def model_to_entity(self, instance: MapperModel) -> MapperEntity: ...

    @abc.abstractmethod
    def entity_to_model(self, instance: MapperEntity) -> MapperModel: ...

