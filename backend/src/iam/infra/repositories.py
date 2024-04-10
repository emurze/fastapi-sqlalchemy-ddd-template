from iam.domain.repositories import IAccountRepository
from iam.domain.entities import Account
from iam.infra.models import AccountModel

from seedwork.infra.repository import SqlAlchemyRepository, InMemoryRepository
from seedwork.domain.mapper import IDataMapper


class AccountMapper(IDataMapper):
    def entity_to_model(self, entity: Account) -> AccountModel:
        dummy_kw = entity.model_dump()
        return AccountModel(**dummy_kw)

    def model_to_entity(self, model: AccountModel) -> Account:
        dummy_kw = model.as_dict()
        return Account(**dummy_kw)


class AccountSqlAlchemyRepository(SqlAlchemyRepository, IAccountRepository):
    mapper_class = AccountMapper
    model_class = AccountModel


class AccountInMemoryRepository(InMemoryRepository, IAccountRepository):
    mapper_class = AccountMapper
