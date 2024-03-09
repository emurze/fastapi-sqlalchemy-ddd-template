import abc
from typing import Any as Model, List


class IPostRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, **kw) -> Model: ...

    @abc.abstractmethod
    async def delete(self, **kw) -> List[Model]: ...

    @abc.abstractmethod
    async def get(self, **kw) -> Model: ...

    @abc.abstractmethod
    async def get_for_update(self, **kw) -> Model: ...

    @abc.abstractmethod
    async def list(self) -> list[Model]: ...


class IPostUnitOfWork(abc.ABC):
    posts: IPostRepository

    @abc.abstractmethod
    async def __aenter__(self) -> None: ...

    @abc.abstractmethod
    async def __aexit__(self, *args) -> None: ...

    @abc.abstractmethod
    async def commit(self) -> None: ...

    @abc.abstractmethod
    async def rollback(self) -> None: ...
