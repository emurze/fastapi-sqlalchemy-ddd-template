from auth.domain.repositories import IAccountRepository
from auth.infra.mappers import AccountMapper
from seedwork.infra.repository import SqlAlchemyRepository, InMemoryRepository
from seedwork.utils.functional import id_int_gen


class AccountSqlAlchemyRepository(SqlAlchemyRepository, IAccountRepository):
    mapper_class = AccountMapper


class AccountInMemoryRepository(InMemoryRepository, IAccountRepository):
    mapper_class = AccountMapper
    field_gens = {
        "id": id_int_gen,
    }
