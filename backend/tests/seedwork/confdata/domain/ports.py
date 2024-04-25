import abc

from seedwork.domain.repositories import ICommandRepository, IQueryRepository
from seedwork.domain.uows import IBaseUnitOfWork


class IExampleCommandRepository(ICommandRepository, abc.ABC):
    pass


class IPostCommandRepository(ICommandRepository, abc.ABC):
    pass


class IExampleQueryRepository(IQueryRepository, abc.ABC):
    pass


class IPostQueryRepository(IQueryRepository, abc.ABC):
    pass


class ITestUnitOfWork(IBaseUnitOfWork, abc.ABC):
    examples: IExampleCommandRepository
    posts: IPostCommandRepository
    query_examples: IExampleQueryRepository
    query_posts: IPostQueryRepository
