from shared.domain.repositories import IGenericRepository
from shared.infra.memory.repository import InMemoryRepository
from shared.infra.memory.uow import InMemoryUnitOfWork
from shared.infra.memory.utils import id_int_gen
from shared.infra.sqlalchemy_orm.repository import SqlAlchemyRepository
from shared.infra.sqlalchemy_orm.uow import SqlAlchemyUnitOfWork
from tests.shared.conftest_data.domain import Example, IExampleUnitOfWork


# In Memory


class ExampleInMemoryRepository(InMemoryRepository, IGenericRepository):
    model = Example
    field_gens = {"id": id_int_gen}


class ExampleInMemoryUnitOfWork(InMemoryUnitOfWork, IExampleUnitOfWork):
    pass


# SqlAlchemy


class ExampleSqlAlchemyRepository(SqlAlchemyRepository, IGenericRepository):
    model = Example


class ExampleSqlAlchemyUnitOfWork(SqlAlchemyUnitOfWork, IExampleUnitOfWork):
    pass
