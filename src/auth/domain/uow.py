import abc

from auth.domain.repositories import IClientRepository


class IAuthUnitOfWork(abc.ABC):
    """Auth unit of work."""

    clients: IClientRepository

    @abc.abstractmethod
    async def __aenter__(self) -> None: ...

    @abc.abstractmethod
    async def __aexit__(self, *args) -> None: ...

    @abc.abstractmethod
    async def commit(self) -> None: ...

    @abc.abstractmethod
    async def rollback(self) -> None: ...
