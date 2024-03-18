import sqlalchemy as sa
from sqlalchemy.orm import registry

from post.domain.entitites import Post
from shared.infra.sqlalchemy_orm.core.contract import DBContract
from shared.utils.functional import get_const

mapper_registry = registry()

post_table = sa.Table(
    "post",
    mapper_registry.metadata,
    sa.Column("id", sa.BigInteger, primary_key=True),
    sa.Column(
        "title",
        sa.String(get_const(Post.title, "max_length")),
        nullable=False,
    ),
    sa.Column(
        "content",
        sa.String(get_const(Post.content, "max_length")),
        nullable=False,
    ),
    sa.Column("draft", sa.Boolean, default=False),
)


def run_mappers():
    mapper_registry.map_imperatively(Post, post_table)


contract = DBContract(
    mapper_runner=run_mappers,
    metadata=mapper_registry.metadata,
)
