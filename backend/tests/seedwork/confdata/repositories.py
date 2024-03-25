from seedwork.domain.repositories import IGenericRepository
from seedwork.infra.repositories import InMemoryRepository, SqlAlchemyRepository
from shared_kernel.utils.functional import id_int_gen
from tests.shared.confdata.entities import Example


class ExampleInMemoryRepository(InMemoryRepository, IGenericRepository):
    aggregate_root = Example
    field_gens = {"id": id_int_gen}


class ExampleSqlAlchemyRepository(SqlAlchemyRepository, IGenericRepository):
    aggregate_root = Example
