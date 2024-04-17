import uuid

from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, MappedColumn, Mapped, relationship

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
    example_id = Column(UUID, ForeignKey("example.id"), nullable=False)
    addresses: Mapped[list['AddressModel']] = relationship()


class AddressModel(Model):
    __tablename__ = "address"
    id = MappedColumn(UUID, primary_key=True, default=next_id)
    city = Column(String, nullable=False)
    example_item_id = Column(
        UUID, ForeignKey("example_item.id"), nullable=False
    )


class ExampleMapper(IDataMapper[Example, ExampleModel]):
    def model_to_entity(self, model: ExampleModel) -> Example:
        return Example(
            **model.as_dict(),
            **model.as_alist(lambda items: [
                ExampleItem(
                    **item.as_dict(),
                    **item.as_alist(lambda addresses: [
                        Address(**addr.as_dict())
                        for addr in addresses
                    ])
                )
                for item in items
            ])
        )

    def update_model(self, entity: Example, model: ExampleModel) -> None:
        model.update(
            **entity.model_dump(exclude={"items"}),
            **entity.only_loaded(lambda items: [
                ExampleItemModel(
                    **item.model_dump(exclude={"addresses"}),
                    **item.only_loaded(lambda addresses: [
                        AddressModel(
                            **addr.model_dump(),
                            example_item_id=item.id
                        )
                        for addr in addresses
                    ]),
                    example_id=entity.id,
                )
                for item in items
            ])
        )


class ExampleSqlAlchemyRepository(SqlAlchemyRepository, IGenericRepository):
    mapper_class = ExampleMapper
    model_class = ExampleModel
