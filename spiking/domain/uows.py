import abc

from seedwork.domain.uows import IBaseUnitOfWork
from spiking.domain.repositories import IPostRepository


class IUnitOfWork(IBaseUnitOfWork, abc.ABC):
    posts: IPostRepository
