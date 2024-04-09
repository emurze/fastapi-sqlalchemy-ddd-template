from orders.domain.entities import Order
from orders.domain.repositories import IOrderRepository
from orders.infra.models import OrderModel, OrderItemModel
from seedwork.domain.collection import alist

from seedwork.domain.mapper import IDataMapper
from seedwork.infra.repository import SqlAlchemyRepository, InMemoryRepository
from seedwork.utils.functional import id_int_gen


class OrderMapper(IDataMapper):
    def entity_to_model(self, entity: Order) -> OrderModel:
        model = OrderModel(
            **entity.model_dump(exclude={"items"}, exclude_deferred=True)
        )
        model.items += (OrderItemModel(**x.model_dump()) for x in entity.items)
        return model

    def model_to_entity(self, model: OrderModel) -> Order:
        return Order(
            **model.as_dict(),
            items=alist(command=[], query=lambda: model.awaitable_attrs.items)
        )


class OrderSqlAlchemyRepository(SqlAlchemyRepository, IOrderRepository):
    mapper_class = OrderMapper
    model_class = OrderModel


class OrderInMemoryRepository(InMemoryRepository, IOrderRepository):
    mapper_class = OrderMapper
    field_gens = {
        "id": id_int_gen,
    }
