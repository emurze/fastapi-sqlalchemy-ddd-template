from seedwork.domain.repositories import IGenericRepository
from seedwork.infra.functional import id_int_gen
from seedwork.infra.repository import InMemoryRepository, SqlAlchemyRepository
from tests.seedwork.confdata.entities import Example


class ExampleInMemoryRepository(InMemoryRepository, IGenericRepository):
    aggregate_root = Example
    field_gens = {"id": id_int_gen}


class ExampleSqlAlchemyRepository(SqlAlchemyRepository, IGenericRepository):
    aggregate_root = Example
