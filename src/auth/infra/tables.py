from datetime import datetime

import sqlalchemy as sa
from sqlalchemy.orm import registry

from auth.domain.entities import Client
from shared.infra.sqlalchemy_orm.core.contract import DBContract

mapper_registry = registry()

client_table = sa.Table(
    "client",
    mapper_registry.metadata,
    sa.Column("id", sa.BigInteger, primary_key=True),
    sa.Column("username", sa.String, nullable=False),
    sa.Column(
        "date_joined",
        sa.TIMESTAMP,
        nullable=False,
        server_default=sa.text("TIMEZONE('utc', now())"),
    ),
    sa.Column(
        "last_login",
        sa.TIMESTAMP,
        nullable=True,
        onupdate=datetime.utcnow,
    ),
)


def run_mappers():
    mapper_registry.map_imperatively(Client, client_table)


contract = DBContract(
    mapper_runner=run_mappers,
    metadata=mapper_registry.metadata,
)
