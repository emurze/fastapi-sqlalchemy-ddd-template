from seedwork.domain.repositories import IGenericRepository
from seedwork.infra.functional import id_int_gen
from seedwork.infra.repository import InMemoryRepository, SqlAlchemyRepository
from tests.seedwork.confdata.entities import Example
from tests.seedwork.confdata.models import ExampleModel


class ExampleInMemoryRepository(InMemoryRepository, IGenericRepository):
    entity_class = Example
    field_gens = {"id": id_int_gen}


class ExampleSqlAlchemyRepository(SqlAlchemyRepository, IGenericRepository):
    entity_class = Example
    model_class = ExampleModel
