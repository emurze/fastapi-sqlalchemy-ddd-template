import abc
from typing import Self

from shared.domain.entities import AggregateRoot
from shared.domain.pydantic_v1 import py_dataclass, Field
from shared.domain.repositories import IGenericRepository


@py_dataclass(kw_only=True)
class Example(AggregateRoot):
    name: str = Field(max_length=10)


class IExampleUnitOfWork(abc.ABC):
    examples: IGenericRepository

    @abc.abstractmethod
    async def __aenter__(self) -> Self: ...

    @abc.abstractmethod
    async def __aexit__(self, *args) -> None: ...

    @abc.abstractmethod
    async def commit(self) -> None: ...

    @abc.abstractmethod
    async def rollback(self) -> None: ...
