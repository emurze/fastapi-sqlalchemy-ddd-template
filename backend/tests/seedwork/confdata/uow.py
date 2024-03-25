import abc

from seedwork.domain.repositories import IGenericRepository
from seedwork.domain.uows import IGenericUnitOfWork


class IExampleRepository(IGenericRepository, abc.ABC):
    pass


class IUnitOfWork(IGenericUnitOfWork, abc.ABC):
    examples: IExampleRepository
