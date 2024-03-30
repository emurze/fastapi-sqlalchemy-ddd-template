import sqlalchemy as sa

from tests.seedwork.confdata.database import TestModel
from tests.seedwork.confdata.entities import Example


class ExampleModel(TestModel):
    __tablename__ = "example"
    id = sa.Column(sa.BIGINT, primary_key=True)
    name = sa.Column(sa.String(Example.c.name.max_length), nullable=False)
