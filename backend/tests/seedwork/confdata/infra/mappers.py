from seedwork.domain.mapper import IDataMapper
from tests.seedwork.confdata.domain.entities import Example
from tests.seedwork.confdata.infra.models import ExampleModel


class ExampleMapper(IDataMapper):
    def entity_to_model(self, entity: Example) -> ExampleModel:
        return ExampleModel(**entity.model_dump())

    def model_to_entity(self, model: ExampleModel) -> Example:
        return Example.model_validate(model)
