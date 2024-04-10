import abc

from seedwork.domain.repositories import IGenericRepository


class IAccountRepository(IGenericRepository, abc.ABC):
    pass
