import abc
from typing import Self

from dataclasses import dataclass

from shared.domain.entities import AggregateRoot


@dataclass(kw_only=True)
class Example(AggregateRoot):
    name: str


class IExampleRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, **kw): ...

    @abc.abstractmethod
    async def get(self, **kw): ...

    @abc.abstractmethod
    async def list(self): ...

    @abc.abstractmethod
    async def delete(self, **kw): ...

    @abc.abstractmethod
    async def delete_one(self, **kw): ...


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
