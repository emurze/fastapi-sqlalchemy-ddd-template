from sqlalchemy import UUID, Column, String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, relationship

from seedwork.domain.services import next_id
from seedwork.infra.database import ModelBase
from tests.seedwork.confdata.domain.entities import Example, ExampleItem


class Model(ModelBase, AsyncAttrs, DeclarativeBase):
    __allow_unmapped__ = True


class ExampleModel(Model):
    __tablename__ = "example"
    id = Column(UUID, primary_key=True, default=next_id)
    name = Column(String, nullable=False)


class ExampleItemModel(Model):
    __tablename__ = "example_item"
    id = Column(UUID, primary_key=True, default=next_id)
    name = Column(String, nullable=False)
    example_id = Column(UUID, ForeignKey("example.id"), nullable=False)


def start_mappers() -> None:
    Model.map_imperatively(
        Example,
        ExampleModel,
        properties={
            "items": relationship(ExampleItem),
        },
    )
    Model.map_imperatively(ExampleItem, ExampleItemModel)
