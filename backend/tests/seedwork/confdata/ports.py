import abc
from typing import Any

from seedwork.domain.repositories import IGenericRepository
from seedwork.domain.uows import IGenericUnitOfWork


class IExampleRepository(IGenericRepository, abc.ABC):
    pass


class ITestUnitOfWork(IGenericUnitOfWork, abc.ABC):
    session: Any
    examples: IExampleRepository
