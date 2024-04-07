import abc

from seedwork.domain.repositories import IGenericRepository


class IOrderRepository(IGenericRepository, abc.ABC):
    pass
