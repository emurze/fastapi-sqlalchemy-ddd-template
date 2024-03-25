import abc

from blog.domain.repositories import IPostRepository
from seedwork.domain.uows import IGenericUnitOfWork


class IUnitOfWork(IGenericUnitOfWork, abc.ABC):
    posts: IPostRepository
