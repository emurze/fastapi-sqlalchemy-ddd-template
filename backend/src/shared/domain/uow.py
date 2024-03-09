import abc
from typing import Self


class IGenericUnitOfWork(abc.ABC):
    """
    examples: IExampleRepository  # Add similar lines to your interface
    """

    @abc.abstractmethod
    async def __aenter__(self) -> Self: ...

    @abc.abstractmethod
    async def __aexit__(self, *args) -> None: ...

    @abc.abstractmethod
    async def commit(self) -> None: ...

    @abc.abstractmethod
    async def rollback(self) -> None: ...
