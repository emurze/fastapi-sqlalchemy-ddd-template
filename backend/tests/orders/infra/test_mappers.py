import pytest

from orders.domain.entities import Order, OrderItem
from orders.infra.models import OrderModel, OrderItemModel
from orders.infra.repositories import OrderMapper
from seedwork.domain.async_structs import alist


class TestOrderMapper:
    mapper = OrderMapper()

    @pytest.mark.unit
    async def test_entity_to_model(self) -> None:
        order_item = OrderItem(price=100, quantity=10)
        entity = Order(id=1, customer_id=1, items=alist([order_item]))
        model = await self.mapper.entity_to_model(entity)
        assert model.id == 1
        assert model.items[0].price == 100
        assert model.items[0].quantity == 10

    @pytest.mark.unit
    async def test_model_to_entity(self) -> None:
        model = OrderModel(id=1, customer_id=1)
        model.items.append(OrderItemModel(price=100, quantity=10))
        order = self.mapper.model_to_entity(model)
        await order.items.load()
        assert order.id == 1
        assert order.items[0].price == 100
        assert order.items[0].quantity == 10
