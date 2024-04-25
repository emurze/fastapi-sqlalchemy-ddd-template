from sqlalchemy.orm import selectinload

from seedwork.infra import repositories as repos
from tests.seedwork.confdata.domain import ports
from tests.seedwork.confdata.infra.mappers import ExampleMapper
from tests.seedwork.confdata.infra.models import ExampleModel, ExampleItemModel


class ExampleSqlAlchemyCommandRepository(
    repos.SqlAlchemyCommandRepository,
    ports.IExampleCommandRepository,
):
    mapper_class = ExampleMapper  # should be default as DefaultMapper
    model_class = ExampleModel


class ExampleSqlAlchemyQueryRepository(
    repos.SqlAlchemyQueryRepository,
    ports.IExampleQueryRepository,
):
    model_class = ExampleModel

    def extend_get_query(self, query):
        return query.options(
            selectinload(self.model_class.items)
            .subqueryload(ExampleItemModel.addresses)
        )


class ExampleInMemoryQueryRepository(  # should be generated
    repos.InMemoryQueryRepository,
    ports.IExampleQueryRepository,
):
    mapper_class = ExampleMapper
    model_class = ExampleModel
