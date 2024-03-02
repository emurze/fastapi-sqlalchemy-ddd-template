import abc
from typing import Any as Model, List


class IGenericRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, **kw) -> Model: ...

    @abc.abstractmethod
    async def get(self, **kw) -> Model: ...

    @abc.abstractmethod
    async def list(self) -> List[Model]: ...

    @abc.abstractmethod
    async def delete(self, **kw) -> List[Model]: ...
