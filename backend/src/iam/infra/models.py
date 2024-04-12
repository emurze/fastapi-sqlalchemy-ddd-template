from sqlalchemy import UUID, Column, String

from iam.domain.entities import Account
from shared.infra.database import Model


class AccountModel(Model):
    __tablename__ = 'account'
    id = Column(UUID, primary_key=True)
    name = Column(String(Account.c.name.max_length), nullable=False)
