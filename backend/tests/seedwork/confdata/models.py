import sqlalchemy as sa

from tests.seedwork.confdata.database import Base


class ExampleModel(Base):
    id = sa.Column("id", sa.BIGINT, primary_key=True)
    name = sa.Column("name", sa.String, nullable=False)
