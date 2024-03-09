import copy
from typing import TypeVar, TypeAlias, Self

from shared.domain.uow import IGenericUnitOfWork

Repository = TypeVar("Repository")
RepositoryList = list[Repository]
RepositoryMemory: TypeAlias = tuple[Repository, list]


class InMemoryUnitOfWork(IGenericUnitOfWork):
    """
    Persists all memory in each repository
    """

    def __init__(self, **repositories: type[Repository]) -> None:
        self._is_committed = False
        self._repositories = self._set_repositories_as_attributes(repositories)
        self._memory_state: list[RepositoryMemory] = [
            (repository, []) for repository in self._repositories
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
        Fixes a new repositories memory state
        """

        self._memory_state = [
            (repository, copy.deepcopy(await repository.list()))
            for repository in self._repositories
        ]
        self._is_committed = True

    async def rollback(self) -> None:
        """
        Rollbacks repositories memory to the last state
        """

        for repository, models in self._memory_state:
            repository._models = copy.deepcopy(models)

    def _set_repositories_as_attributes(self, repositories) -> RepositoryList:
        _repositories = []

        for attribute, repository_cls in repositories.items():
            setattr(self, attribute, repository := repository_cls())
            _repositories.append(repository)

        return _repositories
