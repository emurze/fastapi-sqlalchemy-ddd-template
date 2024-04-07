from sqlalchemy.orm import selectinload

from orders.domain.entities import Order, OrderItem
from orders.domain.repositories import IOrderRepository
from orders.infra.models import OrderModel, OrderItemModel
from seedwork.domain.mapper import IDataMapper
from seedwork.infra.repository import SqlAlchemyRepository, InMemoryRepository
from seedwork.utils.functional import id_int_gen


class OrderMapper(IDataMapper):
    def entity_to_model(self, entity: Order) -> OrderModel:
        model = OrderModel(**entity.model_dump(exclude={"items"}))
        model.items += (OrderItemModel(**x.model_dump()) for x in entity.items)
        return model

    def model_to_entity(self, model: OrderModel) -> Order:
        items = [OrderItem(**x.as_dict()) for x in model.items]
        return Order(**model.as_dict(), items=items)


class OrderSqlAlchemyRepository(SqlAlchemyRepository, IOrderRepository):
    mapper_class = OrderMapper
    model_class = OrderModel

    def _get_by_id_query(self, query):
        return query.options(selectinload(self.model_class.items))


class OrderInMemoryRepository(InMemoryRepository, IOrderRepository):
    mapper_class = OrderMapper
    field_gens = {
        "id": id_int_gen,
    }
