from sqlalchemy import Integer, Column, ForeignKey, UUID
from sqlalchemy.orm import relationship, Mapped

from seedwork.domain.services import next_id
from shared.infra.database import Model


class CustomerModel(Model):
    __tablename__ = "customer"
    id = Column(UUID, primary_key=True, default=next_id)
    account_id = Column(UUID, ForeignKey("account.id"), nullable=False)


class OrderModel(Model):
    __tablename__ = 'order'
    id = Column(UUID, primary_key=True, default=next_id)
    customer_id = Column(UUID, ForeignKey("customer.id"), nullable=False)
    items: Mapped[list['OrderItemModel']] = relationship("OrderItemModel")


class OrderItemModel(Model):
    __tablename__ = 'order_item'
    id = Column(UUID, primary_key=True, default=next_id)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    order_id = Column(UUID, ForeignKey('order.id'), nullable=False)
