import pytest

from orders.domain.entities import Order, OrderItem
from orders.infra.models import OrderModel, OrderItemModel
from orders.infra.repositories import OrderMapper
from seedwork.domain.async_structs import alist
from seedwork.domain.services import next_id


class TestOrderMapper:
    mapper = OrderMapper()

    @pytest.mark.unit
    async def test_model_to_entity(self) -> None:
        model = OrderModel(id=next_id(), customer_id=next_id())
        model.items.append(OrderItemModel(price=100, quantity=10))
        entity = self.mapper.model_to_entity(model)
        await entity.items.load()
        assert entity.id == model.id
        assert entity.customer_id == model.customer_id
        assert entity.items[0].price == 100
        assert entity.items[0].quantity == 10

    @pytest.mark.unit
    def test_entity_to_model(self) -> None:
        entity = Order(
            id=next_id(),
            customer_id=next_id(),
            items=alist([OrderItem(price=100, quantity=10)]),
        )
        model = self.mapper.entity_to_model(entity)
        assert model.id == entity.id
        assert model.customer_id == entity.customer_id
        assert model.items[0].price == 100
        assert model.items[0].quantity == 10

    @pytest.mark.unit
    async def test_entity_appended_item_to_model(self) -> None:
        entity = Order(
            id=next_id(),
            customer_id=next_id(),
        )
        await entity.items.load()
        entity.items.append(OrderItem(price=10, quantity=1))

        model = self.mapper.entity_to_model(entity)
        assert model.id == entity.id
        assert model.customer_id == entity.customer_id
        assert model.items[0].price == 10
        assert model.items[0].quantity == 1

    @pytest.mark.unit
    async def test_entity_with_empty_items_to_model(self) -> None:
        entity = Order(id=next_id(), customer_id=next_id())
        model = self.mapper.entity_to_model(entity)
        assert model.id == entity.id
        assert model.customer_id == entity.customer_id
        assert len(model.items) == 0
