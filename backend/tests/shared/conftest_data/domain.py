import abc
from typing import Self

from pydantic import Field
from pydantic.dataclasses import dataclass

from shared.domain.entities import AggregateRoot
from shared.domain.repositories import IGenericRepository


@dataclass(kw_only=True)
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
