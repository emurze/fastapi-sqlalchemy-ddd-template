import abc
from typing import Self

from tests.shared.domain.repository import IExampleRepository


class IExampleUnitOfWork(abc.ABC):
    examples: IExampleRepository

    @abc.abstractmethod
    async def __aenter__(self) -> Self: ...

    @abc.abstractmethod
    async def __aexit__(self, *args) -> None: ...

    @abc.abstractmethod
    async def commit(self) -> None: ...

    @abc.abstractmethod
    async def rollback(self) -> None: ...
