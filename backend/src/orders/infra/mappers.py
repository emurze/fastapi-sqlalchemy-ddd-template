from orders.domain.entities import Order, OrderItem
from orders.infra.models import OrderModel, OrderItemModel
from seedwork.domain.async_structs import alist
from seedwork.domain.mappers import IDataMapper


class OrderMapper(IDataMapper):
    def model_to_entity(self, model: OrderModel) -> Order:
        async def order_item_factory():
            return [
                OrderItem(**x.as_dict())
                for x in await model.awaitable_attrs.items
            ]

        return Order(
            **model.as_dict(),
            items=alist(order_item_factory)
        )

    def entity_to_model(self, entity: Order) -> OrderModel:
        model = OrderModel(**entity.model_dump(exclude={"items"}))

        def order_item_mapper(instance):
            model.items += [
                OrderItemModel(**x.model_dump(), order_id=model.id)
                for x in instance._list
            ]

        entity.items.map_relation(order_item_mapper)
        return model
