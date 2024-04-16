import abc

from typing import Any as Model, TypeVar, Generic
from seedwork.domain.entities import Entity

TModel = TypeVar('TModel', bound=Model)
TEntity = TypeVar('TEntity', bound=Entity)


class IDataMapper(abc.ABC, Generic[TEntity, TModel]):
    @abc.abstractmethod
    def model_to_entity(self, model: TModel) -> TEntity: ...

    @abc.abstractmethod
    def update_model(self, entity: TEntity, model: TModel) -> TModel: ...
