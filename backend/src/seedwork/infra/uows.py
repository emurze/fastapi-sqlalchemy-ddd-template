import copy
from typing import Iterator, Any, NoReturn, TypeAlias

from collections.abc import Callable
from typing import Self

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.domain.errors import EntityAlreadyExistsError
from seedwork.domain.events import DomainEvent
from seedwork.domain.repositories import IQueryRepository, ICommandRepository
from seedwork.domain.uows import IBaseUnitOfWork

IRepository: TypeAlias = ICommandRepository | IQueryRepository


class CollectEventsMixin:
    _repos: list[IRepository]

    def collect_events(self) -> Iterator[DomainEvent]:
        for repo in self._repos:
            for event in repo.collect_events():
                yield event


class SqlAlchemyUnitOfWork(CollectEventsMixin, IBaseUnitOfWork):
    query_prefix = "query"

    def __init__(
        self,
        session_factory: Callable,
        **repo_classes: dict[str, type[IRepository]],
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
            self._persist_all_repos()
            await self.session.commit()
        except IntegrityError:
            raise EntityAlreadyExistsError()

    async def rollback(self) -> None:
        await self.session.rollback()

    def _persist_all_repos(self) -> None:
        for repo in self._repos:
            repo.persist_all()

    def _set_repos_as_attrs(
        self, session: AsyncSession
    ) -> list[ICommandRepository]:
        command_repos = []
        for name, repos in self._repo_classes.items():
            setattr(self, name, command_repo := repos["command"](session))
            setattr(
                self,
                f"%s_%s" % (self.query_prefix, name),
                repos["query"](session),
            )
            command_repos.append(command_repo)
        return command_repos


class InMemoryUnitOfWork(CollectEventsMixin, IBaseUnitOfWork):
    """
    Persists memory in each repository.
    """

    query_prefix: str = "query"

    def __init__(self, **cls_repos: dict[str, type[IRepository]]) -> None:
        self._is_committed = False
        self._repos: list = self._set_repos_as_attrs(cls_repos)
        self._memory_state: list[tuple[IRepository, dict]] = [
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
            (repo, copy.deepcopy(repo.identity_map)) for repo in self._repos
        ]
        self._is_committed = True

    async def rollback(self) -> None:
        """
        Rollbacks repositories memory to the last state.
        """

        for repository, old_identity_map in self._memory_state:
            repository.identity_map = copy.deepcopy(old_identity_map)

    def _set_repos_as_attrs(self, cls_repos: dict) -> list[ICommandRepository]:
        command_repos = []
        for name, repos_cls in cls_repos.items():
            setattr(self, name, command_repo := repos_cls["command"]())
            setattr(
                self,
                f"%s_%s" % (self.query_prefix, name),
                repos_cls["query"](command_repo.identity_map),
            )
            command_repos.append(command_repo)

        return command_repos
