import abc
from typing import Any as Model, List


class IGenericRepository(abc.ABC):
    @abc.abstractmethod
    async def create(self, **kw) -> None: ...

    @abc.abstractmethod
    async def delete(self, **kw) -> None: ...

    @abc.abstractmethod
    async def get(self, **kw) -> Model: ...

    @abc.abstractmethod
    async def get_for_update(self, **kw) -> Model: ...

    @abc.abstractmethod
    async def list(self) -> List[Model]: ...
