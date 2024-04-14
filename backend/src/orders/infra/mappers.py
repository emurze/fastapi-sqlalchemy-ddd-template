from orders.domain.entities import Order, OrderItem
from orders.infra.models import OrderModel, OrderItemModel
from seedwork.domain.async_structs import alist
from seedwork.domain.mappers import IDataMapper


class OrderMapper(IDataMapper):
    # todo: A new triple relationship

    def model_to_entity(self, model: OrderModel) -> Order:
        async def map_order_item_models_to_entities():
            return [
                OrderItem(**x.as_dict())
                for x in await model.awaitable_attrs.items
            ]

        return Order(
            **model.as_dict(),
            items=alist(coro_factory=map_order_item_models_to_entities)
        )

    def entity_to_model(self, entity: Order) -> OrderModel:
        model = OrderModel(**entity.model_dump(exclude={"items"}))
        model.items += [
            OrderItemModel(**x.model_dump(), order_id=model.id)
            for x in entity.items.loaded_or_load_sync()
        ]
        return model
