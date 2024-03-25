import copy
from typing import TypeVar

from collections.abc import Callable
from typing import Self

from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.domain.uows import IGenericUnitOfWork

Repo = TypeVar("Repo")


class SqlAlchemyUnitOfWork(IGenericUnitOfWork):
    def __init__(self, session_factory: Callable, **repos: type[Repo]) -> None:
        self.session_factory = session_factory
        self._repos = repos

    async def __aenter__(self) -> Self:
        self.session = self.session_factory()
        self._set_repos_as_attrs(self.session)
        return self

    async def __aexit__(self, *args) -> None:
        await self.rollback()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    def _set_repos_as_attrs(self, session: AsyncSession) -> None:
        for attr, repo_cls in self._repos.items():
            setattr(self, attr, repo_cls(session))


class InMemoryUnitOfWork(IGenericUnitOfWork):
    """
    Persists memory in each repository.
    """

    def __init__(self, **repos: type[Repo]) -> None:
        self._is_committed = False
        self._repos = self._set_repos_as_attrs(repos)
        self._memory_state: list[tuple[Repo, list]] = [
            (repo, []) for repo in self._repos
        ]

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args) -> None:
        if self._is_committed:
            self._is_committed = False
        else:
            await self.rollback()

    async def commit(self) -> None:
        """
        Fixes a new repositories memory state.
        """

        self._memory_state = [
            (repo, copy.deepcopy(await repo.list()))
            for repo in self._repos
        ]
        self._is_committed = True

    async def rollback(self) -> None:
        """
        Rollbacks repositories memory to the last state.
        """

        for repository, models in self._memory_state:
            repository._models = copy.deepcopy(models)

    def _set_repos_as_attrs(self, repos: dict[str, type[Repo]]) -> list[Repo]:
        _repos = []

        for attr, repo_cls in repos.items():
            setattr(self, attr, repo := repo_cls())
            _repos.append(repo)

        return _repos
