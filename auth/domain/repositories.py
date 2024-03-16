import abc

from shared.domain.repositories import IGenericRepository
from shared.domain.uows import IGenericUnitOfWork


class IClientRepository(IGenericRepository, abc.ABC):
    pass


class IAuthUnitOfWork(IGenericUnitOfWork, abc.ABC):
    clients: IClientRepository
