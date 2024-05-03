import abc

from seedwork.domain.repositories import IGenericRepository
from seedwork.domain.uows import IBaseUnitOfWork
from tests.seedwork.confdata.domain.entities import Example


class IExampleRepository(IGenericRepository[Example], abc.ABC):
    pass


class ITestUnitOfWork(IBaseUnitOfWork, abc.ABC):
    examples: IExampleRepository
