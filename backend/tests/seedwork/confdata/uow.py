import abc

from seedwork.domain.uows import IGenericUnitOfWork


class IUnitOfWork(IGenericUnitOfWork, abc.ABC):
    examples: O
