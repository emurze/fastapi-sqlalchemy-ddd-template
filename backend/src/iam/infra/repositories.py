from iam.domain.repositories import IAccountRepository
from iam.domain.entities import Account
from iam.infra.models import AccountModel
from seedwork.domain.mappers import IDataMapper

from seedwork.infra.repository import SqlAlchemyRepository, InMemoryRepository


class AccountMapper(IDataMapper):
    async def model_to_entity(self, model: AccountModel) -> Account:
        kw = model.as_dict()
        return Account(**kw)

    async def entity_to_model(self, entity: Account) -> AccountModel:
        kw = entity.model_dump()
        return AccountModel(**kw)


class AccountSqlAlchemyRepository(SqlAlchemyRepository, IAccountRepository):
    mapper_class = AccountMapper
    model_class = AccountModel


class AccountInMemoryRepository(InMemoryRepository, IAccountRepository):
    mapper_class = AccountMapper
