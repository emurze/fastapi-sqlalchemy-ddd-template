from pydantic import PositiveInt

from iam.domain.value_objects import AccountId
from orders.domain.value_objects import OrderId, CustomerId
from seedwork.domain.async_structs import alist
from seedwork.domain.entities import AggregateRoot
from seedwork.domain.services import UUIDField
from seedwork.domain.value_objects import ValueObject


class Customer(AggregateRoot):
    id: CustomerId = UUIDField
    account_id: AccountId

    def make_order(self, **kw) -> 'Order':
        return Order(customer_id=self.id, **kw)


class Order(AggregateRoot):
    id: OrderId = UUIDField
    items: alist['OrderItem'] = alist()
    customer_id: CustomerId

    def add_item(self, **kw) -> None:
        self.items.append(OrderItem(**kw))


class OrderItem(ValueObject):
    price: int
    quantity: PositiveInt
