import abc

from seedwork.domain.repositories import IGenericRepository


class IPostRepository(IGenericRepository, abc.ABC):
    pass
