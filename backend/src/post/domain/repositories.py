import abc

from shared.domain.repositories import IGenericRepository
from shared.domain.uows import IGenericUnitOfWork


class IPostRepository(IGenericRepository, abc.ABC):
    pass


class IPostUnitOfWork(IGenericUnitOfWork, abc.ABC):
    posts: IPostRepository
