from seedwork.domain.repositories import IGenericRepository
from seedwork.utils.functional import id_int_gen
from seedwork.infra.repository import InMemoryRepository, SqlAlchemyRepository
from tests.seedwork.confdata.mappers import ExampleMapper


class ExampleInMemoryRepository(InMemoryRepository, IGenericRepository):
    mapper_class = ExampleMapper
    field_gens = {"id": id_int_gen}


class ExampleSqlAlchemyRepository(SqlAlchemyRepository, IGenericRepository):
    mapper_class = ExampleMapper
