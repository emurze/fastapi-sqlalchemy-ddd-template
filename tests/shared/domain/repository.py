import abc


class IExampleRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, **kw): ...

    @abc.abstractmethod
    async def get(self, **kw): ...

    @abc.abstractmethod
    async def list(self): ...

    @abc.abstractmethod
    async def delete(self, **kw): ...
