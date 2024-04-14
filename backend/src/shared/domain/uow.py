import abc

from iam.domain.repositories import IAccountRepository
from orders.domain.repositories import IOrderRepository
from seedwork.domain.uows import IBaseUnitOfWork


class IUnitOfWork(IBaseUnitOfWork, abc.ABC):
    accounts: IAccountRepository
    orders: IOrderRepository
