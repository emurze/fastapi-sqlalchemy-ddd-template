import sqlalchemy as sa
from sqlalchemy.orm import registry

from tests.shared.conftest_data.domain import Example

mapped_registry = registry()

example_table = sa.Table(
    "example",
    mapped_registry.metadata,
    sa.Column("id", sa.BIGINT, primary_key=True),
    sa.Column("name", sa.String, nullable=False),
)


def run_example_mappers():
    mapped_registry.map_imperatively(Example, example_table)
