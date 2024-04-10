from orders.domain.entities import Order
from orders.domain.repositories import IOrderRepository
from orders.infra.models import OrderModel, OrderItemModel
from seedwork.domain.collection import alist

from seedwork.domain.mapper import IDataMapper
from seedwork.infra.repository import SqlAlchemyRepository, InMemoryRepository


class OrderMapper(IDataMapper):
    async def entity_to_model(self, entity: Order) -> OrderModel:
        print(await entity.items.load())
        model = OrderModel(**entity.model_dump(exclude={"items"}))
        model.items += (
            OrderItemModel(**x.model_dump()) for x in await entity.items.load()
        )
        # todo: Loading is required?
        return model

    def model_to_entity(self, model: OrderModel) -> Order:
        async def _():
            await model.awaitable_attrs.items
            # todo: map to mapper, draw all schema

        return Order(
            **model.as_dict(),
            items=alist(lambda: model.awaitable_attrs.items)
        )


class OrderSqlAlchemyRepository(SqlAlchemyRepository, IOrderRepository):
    mapper_class = OrderMapper
    model_class = OrderModel


class OrderInMemoryRepository(InMemoryRepository, IOrderRepository):
    mapper_class = OrderMapper
