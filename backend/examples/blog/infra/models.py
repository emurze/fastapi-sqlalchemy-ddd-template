import sqlalchemy as sa
from sqlalchemy.orm import registry, relationship

from blog.domain.entitites import Post, Author
from seedwork.infra.database import Model

mapper_registry = registry()


class PostModel(Model):
    __tablename__ = "post"
    id = sa.Column("id", sa.BigInteger, primary_key=True)
    title = sa.Column(
        "title",
        sa.String(Post.c.title.max_length),
        nullable=False,
    )
    content = sa.Column(
        "content",
        sa.String(Post.c.content.max_length),
        nullable=False,
    )
    draft = sa.Column("draft", sa.Boolean, default=False)
    author_id = sa.Column("author_id", sa.Integer, sa.ForeignKey('author.id'))
    author: 'AuthorModel' = relationship('AuthorModel', back_populates="posts")


class AuthorModel(Model):
    __tablename__ = "author"
    id = sa.Column("id", sa.BigInteger, primary_key=True)
    posts: list[PostModel] = relationship(
        PostModel,
        back_populates="author",
        innerjoin=True,
    )
