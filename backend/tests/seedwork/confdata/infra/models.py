from sqlalchemy import UUID, Column, String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship

from seedwork.domain.services import next_id
from seedwork.infra.database import ModelBase
from tests.seedwork.confdata.domain.entities import Example


class Model(ModelBase, AsyncAttrs, DeclarativeBase):
    __allow_unmapped__ = True


class ExampleModel(Model):
    __tablename__ = 'example'
    id = Column(UUID, primary_key=True, default=next_id)
    name = Column(String(Example.c.name.max_length), nullable=False)
    items: Mapped[list['ExampleItemModel']] = relationship(
        cascade="all, delete-orphan",
    )


class ExampleItemModel(Model):
    __tablename__ = 'example_item'
    id = Column(UUID, primary_key=True, default=next_id)
    name = Column(String, nullable=False)
    example_id = Column(UUID, ForeignKey("example.id"), nullable=False)
    addresses: Mapped[list['AddressModel']] = relationship(
        cascade="all, delete-orphan",
    )


class AddressModel(Model):
    __tablename__ = 'address'
    id = Column(UUID, primary_key=True, default=next_id)
    city = Column(String, nullable=False)
    example_item_id = Column(
        UUID, ForeignKey("example_item.id"), nullable=False
    )


class PostModel(Model):
    __tablename__ = 'post'
    id = Column(UUID, primary_key=True, default=next_id)
    title = Column(String(256))
    comments: Mapped[list['CommentModel']] = relationship(
        secondary="post_comment",
        cascade="all, delete-orphan",
    )


class PostCommentModel(Model):
    __tablename__ = 'post_comment'
    post_id = Column(UUID, ForeignKey('post.id', ondelete="CASCADE"), primary_key=True)
    comment_id = Column(UUID, ForeignKey('comment.id', ondelete="CASCADE"), primary_key=True)


class CommentModel(Model):
    __tablename__ = 'comment'
    id = Column(UUID, primary_key=True, default=next_id)
    body = Column(String(256))
