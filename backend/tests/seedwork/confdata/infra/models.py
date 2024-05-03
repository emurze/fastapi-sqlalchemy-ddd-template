from sqlalchemy import UUID, Column, String, ForeignKey, Table
from sqlalchemy.orm import registry, relationship

from seedwork.domain.services import next_id
from tests.seedwork.confdata.domain.entities import Example, ExampleItem

mapped_registry = registry()

example_table = Table(
    "example",
    mapped_registry.metadata,
    Column("id", UUID, primary_key=True, default=next_id),
    Column("name", String, nullable=False),
)

example_item_table = Table(
    "example_item",
    mapped_registry.metadata,
    Column("id", UUID, primary_key=True, default=next_id),
    Column("name", String, nullable=False),
    Column(
        "example_id",
        UUID,
        ForeignKey("example.id", ondelete="CASCADE"),
        nullable=False
    ),
)


def start_mappers() -> None:
    mapped_registry.map_imperatively(
        ExampleItem,
        example_item_table,
    )
    mapped_registry.map_imperatively(
        Example,
        example_table,
        properties={
            "items": relationship(ExampleItem, backref="example", cascade="all, delete"),
        },
    )
