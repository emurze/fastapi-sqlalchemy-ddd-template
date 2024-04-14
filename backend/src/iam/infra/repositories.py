from iam.domain.repositories import IAccountRepository
from iam.infra.mappers import AccountMapper
from iam.infra.models import AccountModel

from seedwork.infra.repository import SqlAlchemyRepository


class AccountSqlAlchemyRepository(SqlAlchemyRepository, IAccountRepository):
    mapper_class = AccountMapper
    model_class = AccountModel
