import abc

from seedwork.domain.repositories import IGenericRepository
from seedwork.domain.uows import IBaseUnitOfWork


class IExampleRepository(IGenericRepository, abc.ABC):
    pass


class ITestUnitOfWork(IBaseUnitOfWork, abc.ABC):
    examples: IExampleRepository

