import abc
from collections.abc import Iterator, Callable
from typing import Self

from auth.domain.repositories import IAccountRepository
from seedwork.domain.events import Event


class IGenericUnitOfWork(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def __aenter__(self) -> Self: ...

    @abc.abstractmethod
    async def __aexit__(self, *args) -> None: ...

    @abc.abstractmethod
    async def commit(self) -> None: ...

    @abc.abstractmethod
    async def rollback(self) -> None: ...

    @abc.abstractmethod
    def collect_events(self) -> Iterator[Event]: ...


class IUnitOfWork(IGenericUnitOfWork, abc.ABC):
    accounts: IAccountRepository


UnitOfWorkFactory = Callable[[], IUnitOfWork]
