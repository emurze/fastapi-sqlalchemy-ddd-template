import abc
from typing import Self

from blog.domain.repositories import IPostRepository


class IGenericUnitOfWork(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def __aenter__(self) -> Self: ...

    @abc.abstractmethod
    async def __aexit__(self, *args) -> None: ...

    @abc.abstractmethod
    async def commit(self) -> None: ...

    @abc.abstractmethod
    async def rollback(self) -> None: ...


class IUnitOfWork(IGenericUnitOfWork, abc.ABC):
    posts: IPostRepository
