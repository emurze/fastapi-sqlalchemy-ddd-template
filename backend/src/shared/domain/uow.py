import abc
from typing import Any

from iam.domain.repositories import IAccountRepository
from orders.domain.repositories import IOrderRepository
from seedwork.domain.uows import IGenericUnitOfWork


class IUnitOfWork(IGenericUnitOfWork, abc.ABC):
    session: Any
    accounts: IAccountRepository
    orders: IOrderRepository
