import abc

from iam.domain.entities import Account
from seedwork.domain.repositories import IGenericRepository


class IAccountRepository(IGenericRepository[Account], abc.ABC):
    pass
