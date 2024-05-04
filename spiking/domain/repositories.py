import abc

from seedwork.domain.repositories import IGenericRepository
from spiking.domain.entities import Post


class IPostRepository(IGenericRepository[Post], abc.ABC):
    pass
