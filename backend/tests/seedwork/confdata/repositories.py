import uuid

from sqlalchemy import Column, String, UUID, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedColumn,
    Mapped,
    relationship,
    selectinload,
)

from seedwork.domain.mappers import IDataMapper
from seedwork.domain.services import next_id
from seedwork.infra.database import ModelBase
from seedwork.infra.repositories import (
    SqlAlchemyCommandRepository,
    SqlAlchemyQueryRepository,
    InMemoryQueryRepository,
)
from .domain import Example, ExampleItem, Address
from .ports import (
    IExampleCommandRepository,
    IExampleQueryRepository,
)


class Model(ModelBase, AsyncAttrs, DeclarativeBase):
    __allow_unmapped__ = True
    id: Mapped[uuid.UUID]


class ExampleModel(Model):
    __tablename__ = 'example'
    id = MappedColumn(UUID, primary_key=True, default=next_id)
    name = Column(String(Example.c.name.max_length), nullable=False)
    items: Mapped[list['ExampleItemModel']] = relationship(
        cascade="all, delete-orphan",
        passive_updates=True,
    )


class ExampleItemModel(Model):
    __tablename__ = 'example_item'
    id = MappedColumn(UUID, primary_key=True, default=next_id)
    name = Column(String, nullable=False)
    example_id = Column(UUID, ForeignKey("example.id"), nullable=False)
    addresses: Mapped[list['AddressModel']] = relationship(
        cascade="all, delete-orphan",
        passive_updates=True,
    )


class AddressModel(Model):
    __tablename__ = 'address'
    id = MappedColumn(UUID, primary_key=True, default=next_id)
    city = Column(String, nullable=False)
    example_item_id = Column(
        UUID, ForeignKey("example_item.id"), nullable=False
    )


class ExampleMapper(IDataMapper[Example, ExampleModel]):  # should be generated
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
            **entity.persist(lambda items: [
                ExampleItemModel(
                    **item.model_dump(exclude={"addresses"}),
                    **item.persist(lambda addresses: [
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


class ExampleSqlAlchemyCommandRepository(
    SqlAlchemyCommandRepository,
    IExampleCommandRepository,
):
    mapper_class = ExampleMapper  # should be default as DefaultMapper
    model_class = ExampleModel


class ExampleSqlAlchemyQueryRepository(
    SqlAlchemyQueryRepository,
    IExampleQueryRepository,
):
    model_class = ExampleModel

    def extend_get_query(self, query):
        return query.options(
            selectinload(self.model_class.items)
            .subqueryload(ExampleItemModel.addresses)
        )


class ExampleInMemoryQueryRepository(  # should be generated
    InMemoryQueryRepository,
    IExampleQueryRepository,
):
    mapper_class = ExampleMapper
    model_class = ExampleModel
