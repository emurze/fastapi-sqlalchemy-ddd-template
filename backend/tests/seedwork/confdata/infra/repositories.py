from sqlalchemy.orm import selectinload

from seedwork.infra import repositories as repos
from tests.seedwork.confdata.domain import ports
from tests.seedwork.confdata.infra import mappers
from tests.seedwork.confdata.infra import models


class ExampleSqlAlchemyCommandRepository(
    repos.SqlAlchemyCommandRepository,
    ports.IExampleCommandRepository,
):
    mapper_class = mappers.ExampleMapper  # should be default as DefaultMapper
    model_class = models.ExampleModel


class ExampleSqlAlchemyQueryRepository(
    repos.SqlAlchemyQueryRepository,
    ports.IExampleQueryRepository,
):
    model_class = models.ExampleModel

    def extend_get_query(self, query):
        return query.options(
            selectinload(self.model_class.items)
            .subqueryload(models.ExampleItemModel.addresses)
        )


class PostSqlAlchemyCommandRepository(
    repos.SqlAlchemyCommandRepository,
    ports.IPostCommandRepository,
):
    mapper_class = mappers.PostMapper
    model_class = models.PostModel


class PostSqlAlchemyQueryRepository(
    repos.SqlAlchemyQueryRepository,
    ports.IPostQueryRepository,
):
    model_class = models.PostModel
