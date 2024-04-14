from sqlalchemy import Column, String, UUID

from iam.domain.entities import Account
from seedwork.domain.services import next_id
from shared.infra.database import Model


class AccountModel(Model):
    __tablename__ = 'account'
    id = Column(UUID, primary_key=True, default=next_id)
    name = Column(String(Account.c.name.max_length), nullable=False)
