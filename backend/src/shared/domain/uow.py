import abc

from seedwork.domain.uows import IBaseUnitOfWork


class IUnitOfWork(IBaseUnitOfWork, abc.ABC):
    """
    Usage:
        class IUnitOfWork(IBaseUnitOfWork, abc.ABC):
            examples: IExampleRepository
    """
