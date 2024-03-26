import sqlalchemy as sa
from sqlalchemy import ForeignKey, Integer, Column
from sqlalchemy.orm import registry, relationship

from blog.domain.entitites import Post, Publisher
from seedwork.infra.database import Model
from seedwork.infra.functional import get_const

mapper_registry = registry()


class PostModel(Model):
    __tablename__ = "post"
    id = sa.Column("id", sa.BigInteger, primary_key=True)
    title = sa.Column(
        "title",
        sa.String(get_const(Post, "title.max_length")),
        nullable=False,
    )
    content = sa.Column(
        "content",
        sa.String(get_const(Post, "content.max_length")),
        nullable=False,
    )
    draft = sa.Column("draft", sa.Boolean, default=False)
    # publisher_id = Column(Integer, ForeignKey('publisher.id'))
    #
    # publisher: 'PublisherModel' = relationship(
    #     'PublisherModel',
    #     back_populates="posts",
    # )


class PublisherModel(Model):
    __tablename__ = "publisher"
    id = sa.Column("id", sa.BigInteger, primary_key=True)
    name = sa.Column(
        "name",
        sa.String(get_const(Publisher, "name.max_length")),
        unique=True,
        nullable=False,
    )

    # posts: list[PostModel] = relationship(
    #     PostModel,
    #     back_populates="publisher",
    #     innerjoin=True,
    # )
