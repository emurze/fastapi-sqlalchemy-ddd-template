from seedwork.domain.repositories import IGenericRepository
from seedwork.infra.repository import InMemoryRepository, SqlAlchemyRepository
from tests.seedwork.confdata.infra.mappers import ExampleMapper
from tests.seedwork.confdata.infra.models import ExampleModel


class ExampleSqlAlchemyRepository(SqlAlchemyRepository, IGenericRepository):
    mapper_class = ExampleMapper
    model_class = ExampleModel


class ExampleInMemoryRepository(InMemoryRepository, IGenericRepository):
    mapper_class = ExampleMapper
