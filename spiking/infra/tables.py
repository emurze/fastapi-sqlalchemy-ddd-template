from sqlalchemy import Table, Column, String, UUID, Integer, Boolean, \
    ForeignKey
from sqlalchemy.orm import relationship

from seedwork.domain.services import next_id
from spiking.domain.entities import Post, Author
from spiking.infra.database import mapped_registry

post_table = Table(
    "post",
    mapped_registry.metadata,
    Column("id", UUID, primary_key=True, default=next_id),
    Column("name", String, nullable=False),
    Column("description", String, nullable=False),
    Column("rate", Integer, nullable=False),
    Column("photo", String, nullable=True),
    Column("draft", Boolean, default=True),
)

post_author_table = Table(
    "post_author",
    mapped_registry.metadata,
    Column(
        "post_id",
        UUID,
        ForeignKey("post.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "author_id",
        UUID,
        ForeignKey("author.id", ondelete="CASCADE"),
        primary_key=True
    ),
)

author_table = Table(
    "author",
    mapped_registry.metadata,
    Column("id", UUID, primary_key=True, default=next_id),
    Column("name", String, nullable=False),
)


def start_mappers() -> None:
    mapped_registry.map_imperatively(
        Post,
        post_table,
        properties={
            "authors": relationship(Author, secondary=post_author_table),
        }
    )
    mapped_registry.map_imperatively(Author, author_table)
