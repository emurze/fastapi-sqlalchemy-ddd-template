from seedwork.infra.repository import SqlAlchemyRepository
from tests.seedwork.confdata.domain.entities import Example
from tests.seedwork.confdata.domain.ports import IExampleRepository


class ExampleSqlAlchemyRepository(SqlAlchemyRepository, IExampleRepository):
    entity_class = Example
