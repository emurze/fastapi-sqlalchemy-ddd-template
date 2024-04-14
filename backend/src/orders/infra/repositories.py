from orders.domain.repositories import IOrderRepository
from orders.infra.mappers import OrderMapper
from orders.infra.models import OrderModel

from seedwork.infra.repository import SqlAlchemyRepository


class OrderSqlAlchemyRepository(SqlAlchemyRepository, IOrderRepository):
    mapper_class = OrderMapper
    model_class = OrderModel
