import copy
from typing import Iterator, Any, NoReturn

from collections.abc import Callable
from typing import Self

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.domain.errors import EntityAlreadyExistsError
from seedwork.domain.events import Event
from seedwork.domain.repositories import IGenericRepository
from seedwork.domain.uows import IBaseUnitOfWork


class CollectEventsMixin:
    _repos: list[IGenericRepository]

    def collect_events(self) -> Iterator[Event]:
        for repo in self._repos:
            for event in repo.collect_events():
                yield event


class SqlAlchemyUnitOfWork(CollectEventsMixin, IBaseUnitOfWork):
    def __init__(self, session_factory: Callable, **repo_classes) -> None:
        self._repo_classes = repo_classes
        self._session_factory = session_factory
        self.session: Any = None

    async def __aenter__(self) -> Self:
        self.session = self._session_factory()
        self._repos = self._set_repos_as_attrs(self.session)
        return self

    async def __aexit__(self, *args) -> None:
        await self.rollback()
        await self.session.close()

    async def commit(self) -> NoReturn | None:
        try:
            await self._persist_all_repos()
            await self.session.commit()
        except IntegrityError as e:
            print(e)
            raise EntityAlreadyExistsError()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def _persist_all_repos(self) -> None:
        for repo in self._repos:
            await repo.persist_all()

    def _set_repos_as_attrs(self, session: AsyncSession) -> list:
        _repos = []
        for attr, repo_cls in self._repo_classes.items():
            setattr(self, attr, repo := repo_cls(session))
            _repos.append(repo)
        return _repos


class InMemoryUnitOfWork(CollectEventsMixin, IBaseUnitOfWork):
    """
    Persists memory in each repository.
    """

    def __init__(self, **repo_classes: type[IGenericRepository]) -> None:
        self._is_committed = False
        self._repos: list = self._set_repos_as_attrs(repo_classes)
        self._memory_state: list[tuple[IGenericRepository, dict]] = [
            (repo, {}) for repo in self._repos
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
            (repo, copy.deepcopy(repo.identity_map))
            for repo in self._repos
        ]
        self._is_committed = True

    async def rollback(self) -> None:
        """
        Rollbacks repositories memory to the last state.
        """

        for repository, old_identity_map in self._memory_state:
            repository.identity_map = copy.deepcopy(old_identity_map)

    def _set_repos_as_attrs(self, cls_repos: dict) -> list[IGenericRepository]:
        _repos = []
        for attr, repo_cls in cls_repos.items():
            setattr(self, attr, repo := repo_cls())
            _repos.append(repo)
        return _repos
