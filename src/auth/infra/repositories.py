from auth.domain.entities import Client
from auth.domain.repositories import IClientRepository
from auth.domain.uow import IAuthUnitOfWork
from shared.infra.memory.repository import InMemoryRepository
from shared.infra.memory.uow import InMemoryUnitOfWork
from shared.infra.memory.utils import id_int_gen, create_at_gen
from shared.infra.sqlalchemy_orm.repository import SqlAlchemyRepository
from shared.infra.sqlalchemy_orm.uow import SqlAlchemyUnitOfWork


class ClientSqlAlchemyRepository(SqlAlchemyRepository, IClientRepository):
    pass


class AuthSqlAlchemyUnitOfWork(SqlAlchemyUnitOfWork, IAuthUnitOfWork):
    pass


class ClientInMemoryRepository(InMemoryRepository, IClientRepository):
    model = Client
    field_gens = {
        "id": id_int_gen,
        "date_joined": create_at_gen,
    }


class AuthInMemoryUnitOfWork(InMemoryUnitOfWork, IAuthUnitOfWork):
    pass
