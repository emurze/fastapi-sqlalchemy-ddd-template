from auth.domain.entities import Client
from auth.domain.repository import IClientRepository
from auth.domain.uow import IAuthUnitOfWork
from shared.infra.sqlalchemy_orm.repository import SqlAlchemyRepository
from shared.infra.sqlalchemy_orm.uow import SqlAlchemyUnitOfWork


class ClientSqlAlchemyRepository(SqlAlchemyRepository, IClientRepository):
    model = Client


class AuthSqlAlchemyUnitOfWork(SqlAlchemyUnitOfWork, IAuthUnitOfWork):
    pass
