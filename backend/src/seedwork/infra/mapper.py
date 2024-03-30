from seedwork.domain.entities import Entity
from seedwork.domain.mapper import IDataMapper
from seedwork.infra.database import Model


class DataMapper(IDataMapper):
    entity_class: type[Entity]
    model_class: type[Model]

    def entity_to_model(self, entity: Entity) -> Model:
        return self.model_class(**entity.model_dump())

    def model_to_entity(self, model: Model) -> Entity:
        return self.entity_class.model_validate(model)
