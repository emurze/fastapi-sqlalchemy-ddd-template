import sqlalchemy as sa

from iam.domain.entities import Account
from seedwork.infra.database import Model


class AccountModel(Model):
    __tablename__ = 'account'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String(Account.c.name.max_length), nullable=False)
