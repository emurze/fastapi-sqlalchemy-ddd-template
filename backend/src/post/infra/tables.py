import sqlalchemy as sa
from sqlalchemy.orm import registry

from post.domain.entitites import Post
from shared.infra.sqlalchemy_orm.core.contract import DBContract

mapper_registry = registry()

post_table = sa.Table(
    "client",
    mapper_registry.metadata,
    sa.Column("id", sa.BigInteger, primary_key=True),
    sa.Column("title", sa.String(length=256), nullable=False),
    sa.Column("content", sa.String(length=256), nullable=False),
    sa.Column("draft", sa.Boolean, default=False),
)


def run_mappers():
    mapper_registry.map_imperatively(Post, post_table)


contract = DBContract(
    mapper_runner=run_mappers,
    metadata=mapper_registry.metadata,
)
