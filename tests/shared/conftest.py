import abc
from typing import Self, Any as Model, List

from dataclasses import dataclass
from shared.domain.entities import AggregateRoot


@dataclass(kw_only=True)
class Example(AggregateRoot):
    name: str


class IExampleRepository(abc.ABC):
    @abc.abstractmethod
    async def get(self, **kw) -> Model: ...

    @abc.abstractmethod
    async def get_for_update(self, **kw) -> Model: ...

    @abc.abstractmethod
    async def list(self) -> list[Model]: ...

    @abc.abstractmethod
    async def add(self, **kw) -> Model: ...

    @abc.abstractmethod
    async def delete_one(self, **kw) -> Model: ...

    @abc.abstractmethod
    async def delete(self, **kw) -> List[Model]: ...


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
