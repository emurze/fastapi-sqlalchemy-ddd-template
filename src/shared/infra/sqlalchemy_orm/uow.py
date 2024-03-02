from collections.abc import Callable
from typing import TypeAlias, Self

from sqlalchemy.ext.asyncio import AsyncSession

from shared.domain.uow import IGenericUnitOfWork

cls: TypeAlias = type


class SqlAlchemyUnitOfWork(IGenericUnitOfWork):
    def __init__(self, session_factory: Callable, **repositories: cls) -> None:
        self.session_factory = session_factory
        self._repositories = repositories

    async def __aenter__(self) -> Self:
        self.session = self.session_factory()
        self._set_repositories_as_attributes(self.session)
        return self

    async def __aexit__(self, *args) -> None:
        await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    def _set_repositories_as_attributes(self, session: AsyncSession) -> None:
        for attribute, repository_cls in self._repositories.items():
            setattr(self, attribute, repository_cls(session))
