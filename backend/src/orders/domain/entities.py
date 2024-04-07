from pydantic import PositiveInt

from auth.domain.value_objects import AccountId
from orders.domain.value_objects import OrderId, CustomerId
from seedwork.domain.entities import AggregateRoot
from seedwork.domain.value_objects import defer, Deferred, ValueObject


class Customer(AggregateRoot):
    id: defer[CustomerId] = Deferred
    account_id: AccountId

    def make_order(self, **kw) -> 'Order':
        return Order(customer_id=self.id, **kw)


class Order(AggregateRoot):
    id: defer[OrderId] = Deferred
    items: list['OrderItem'] = []
    customer_id: CustomerId


class OrderItem(ValueObject):
    price: int
    quantity: PositiveInt
