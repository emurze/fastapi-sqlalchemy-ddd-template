from orders.domain.entities import Order
from orders.domain.repositories import IOrderRepository
from orders.infra.models import OrderModel, OrderItemModel
from seedwork.domain.async_structs import alist
from seedwork.domain.mappers import IDataMapper

from seedwork.infra.repository import SqlAlchemyRepository, InMemoryRepository


class OrderMapper(IDataMapper):
    async def entity_to_model(self, entity: Order) -> OrderModel:
        model = OrderModel(**entity.model_dump(exclude={"items"}))

        if model.items.is_loaded:
            model.items += (  # better operation
                OrderItemModel(**x.model_dump()) for x in entity.items
            )

        return model

    def model_to_entity(self, model: OrderModel) -> Order:
        return Order(
            **model.as_dict(),
            items=alist(lambda: model.awaitable_attrs.items)
        )


class OrderSqlAlchemyRepository(SqlAlchemyRepository, IOrderRepository):
    mapper_class = OrderMapper
    model_class = OrderModel


class OrderInMemoryRepository(InMemoryRepository, IOrderRepository):
    mapper_class = OrderMapper
