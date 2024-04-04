from seedwork.domain.mapper import IDataMapper
from tests.seedwork.confdata.domain.entities import Example
from tests.seedwork.confdata.infra.models import ExampleModel


class ExampleMapper(IDataMapper):
    entity_class = Example
    model_class = ExampleModel

    def entity_to_model(self, entity: Example) -> ExampleModel:
        return self.model_class(**entity.model_dump())

    def model_to_entity(self, model: ExampleModel) -> Example:
        return self.entity_class.model_validate(model)
