import abc

from seedwork.domain.uows import IBaseUnitOfWork


class IUnitOfWork(IBaseUnitOfWork, abc.ABC):
    # accounts: IAccountRepository
    # orders: IOrderRepository
    pass
