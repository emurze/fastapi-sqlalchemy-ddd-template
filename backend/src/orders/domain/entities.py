from pydantic import PositiveInt

from iam.domain.value_objects import AccountId
from orders.domain.value_objects import OrderId, CustomerId
from seedwork.domain.collection import alist
from seedwork.domain.entities import AggregateRoot
from seedwork.domain.value_objects import ValueObject


class Customer(AggregateRoot):
    id: CustomerId
    account_id: AccountId

    def make_order(self, **kw) -> 'Order':
        return Order(customer_id=self.id, **kw)


class Order(AggregateRoot):
    id: OrderId
    items: alist['OrderItem'] = alist()
    customer_id: CustomerId

    def add_item(self, **kw) -> None:
        self.items.append(OrderItem(**kw))

    async def run_by_items(self) -> None:
        for item in await self.items.load():
            print(item)


class OrderItem(ValueObject):
    price: int
    quantity: PositiveInt