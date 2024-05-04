import copy
from typing import Iterator, Any, NoReturn

from collections.abc import Callable
from typing import Self

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.domain.errors import EntityAlreadyExistsError
from seedwork.domain.events import DomainEvent
from seedwork.domain.repositories import IGenericRepository
from seedwork.domain.uows import IBaseUnitOfWork


class CollectEventsMixin:
    _repos: list[IGenericRepository]

    def collect_events(self) -> Iterator[DomainEvent]:
        for repo in self._repos:
            for event in repo.collect_events():
                yield event


class SqlAlchemyUnitOfWork(CollectEventsMixin, IBaseUnitOfWork):
    """Persists data in database."""

    def __init__(
        self,
        session_factory: Callable,
        **repo_classes: dict[str, type[IGenericRepository]],
    ) -> None:
        self._repo_classes: dict = repo_classes
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
            await self.session.commit()
        except IntegrityError:
            raise EntityAlreadyExistsError()

    async def rollback(self) -> None:
        await self.session.rollback()

    def _set_repos_as_attrs(
        self, session: AsyncSession
    ) -> list[IGenericRepository]:
        """Sets repositories as attributes of the unit of work."""
        command_repos = []
        for name, repo_cls in self._repo_classes.items():
            setattr(self, name, command_repo := repo_cls(session))
            command_repos.append(command_repo)
        return command_repos


class InMemoryUnitOfWork(CollectEventsMixin, IBaseUnitOfWork):
    """Persists memory in each repository."""

    def __init__(self, **cls_repos: type[IGenericRepository]) -> None:
        self._is_committed = False
        self._repos: list = self._set_repos_as_attrs(cls_repos)
        self._memory_state: list[tuple[IGenericRepository, dict]] = [
            (repo, {}) for repo in self._repos
        ]

    async def __aenter__(self) -> Self:
        self.override_getters()
        return self

    async def __aexit__(self, *args) -> None:
        if self._is_committed:
            self._is_committed = False
        else:
            await self.rollback()
        self.restore_getters()

    async def commit(self) -> None:
        """Fixes a new repositories memory state."""
        self._memory_state = [
            (repo, copy.deepcopy(repo.identity_map)) for repo in self._repos
        ]
        self._is_committed = True

    async def rollback(self) -> None:
        """Rollbacks repositories memory to the last state."""
        for repository, old_identity_map in self._memory_state:
            repository.identity_map = copy.deepcopy(old_identity_map)

    def override_getters(self) -> None:
        """
        Overrides entity_class getters to raise errors
        when accessing unloaded lazy attributes and relations.
        """
        for repo in self._repos:
            repo.override_getter()

    def restore_getters(self) -> None:
        """Restores entity_class getters to their previous state."""
        for repo in self._repos:
            repo.restore_getter()

    def _set_repos_as_attrs(self, cls_repos: dict) -> list[IGenericRepository]:
        """Sets repositories as attributes of the unit of work."""
        command_repos = []
        for name, repo_cls in cls_repos.items():
            setattr(self, name, command_repo := repo_cls())
            command_repos.append(command_repo)
        return command_repos
