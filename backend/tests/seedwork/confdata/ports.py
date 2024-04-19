import abc

from seedwork.domain.repositories import ICommandRepository, IQueryRepository
from seedwork.domain.uows import IBaseUnitOfWork


class IExampleCommandRepository(ICommandRepository, abc.ABC):
    pass


class IExampleQueryRepository(IQueryRepository, abc.ABC):
    pass


class ITestUnitOfWork(IBaseUnitOfWork, abc.ABC):
    examples: IExampleCommandRepository
    query_examples: IExampleQueryRepository
