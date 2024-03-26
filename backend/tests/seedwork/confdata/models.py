import sqlalchemy as sa

from tests.seedwork.confdata.database import TestModel


class ExampleModel(TestModel):
    __tablename__ = "example"
    id = sa.Column("id", sa.BIGINT, primary_key=True)
    name = sa.Column("name", sa.String, nullable=False)
