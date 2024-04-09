from sqlalchemy import Integer, Column, ForeignKey
from sqlalchemy.orm import relationship, Mapped

from seedwork.infra.database import Model


class CustomerModel(Model):
    __tablename__ = "customer"
    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("account.id"), nullable=False)


class OrderModel(Model):
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customer.id"), nullable=False)
    items: Mapped[list['OrderItemModel']] = relationship("OrderItemModel")


class OrderItemModel(Model):
    __tablename__ = 'order_item'
    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
