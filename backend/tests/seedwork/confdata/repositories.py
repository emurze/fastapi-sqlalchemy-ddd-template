import uuid

from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, MappedColumn, Mapped, relationship

from seedwork.domain.async_structs import alist
from seedwork.domain.mappers import IDataMapper
from seedwork.domain.repositories import IGenericRepository
from seedwork.domain.services import next_id
from seedwork.infra.database import ModelBase
from seedwork.infra.repository import SqlAlchemyRepository
from tests.seedwork.confdata.domain import Example, ExampleItem, Address


class Model(ModelBase, AsyncAttrs, DeclarativeBase):
    __allow_unmapped__ = True
    id: Mapped[uuid.UUID]


class ExampleModel(Model):
    __tablename__ = "example"
    id = MappedColumn(UUID, primary_key=True, default=next_id)
    name = Column(String(Example.c.name.max_length), nullable=False)
    items: Mapped[list['ExampleItemModel']] = relationship()


class ExampleItemModel(Model):
    __tablename__ = "example_item"
    id = MappedColumn(UUID, primary_key=True, default=next_id)
    name = Column(String, nullable=False)
    example_id = Column(String, ForeignKey("example.id"), nullable=False)
    addresses: Mapped[list['AddressModel']] = relationship()


class AddressModel(Model):
    __tablename__ = "address"
    id = MappedColumn(UUID, primary_key=True, default=next_id)
    city = Column(String, nullable=False)
    example_item_id = Column(
        String, ForeignKey("example_item.id"), nullable=False
    )


class ExampleMapper(IDataMapper):
    def model_to_entity(self, model: ExampleModel) -> Example:
        async def map_address(example_item) -> list[Address]:
            return [
                Address(**x.as_dict())
                for x in await example_item.awaitable_attrs.addresses
            ]

        async def map_example_item() -> list[ExampleItem]:
            return [
                ExampleItem(
                    **x.as_dict(),
                    addresses=alist(coro_factory=lambda: map_address(x)),
                )
                for x in await model.awaitable_attrs.items
            ]

        return Example(
            **model.as_dict(),
            items=alist(coro_factory=map_example_item)
        )

    def entity_to_model(self, entity: Example) -> ExampleModel:
        return ExampleModel(
            **entity.model_dump(exclude={"items"}),
            items=[
                ExampleItemModel(
                    **item.model_dump(exclude={"addresses"}),
                    example_id=str(entity.id),
                    addresses=[
                        AddressModel(
                            **addr.model_dump(),
                            example_item_id=str(item.id)
                        )
                        for addr in item.addresses.loaded_or_load_sync()
                    ]
                )
                for item in entity.items.loaded_or_load_sync()
            ]
        )


class ExampleSqlAlchemyRepository(SqlAlchemyRepository, IGenericRepository):
    mapper_class = ExampleMapper
    model_class = ExampleModel
