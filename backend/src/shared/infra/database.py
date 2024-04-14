import uuid

from sqlalchemy import Column, UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from seedwork.domain.services import next_id
from seedwork.infra.database import ModelBase


class Model(ModelBase, AsyncAttrs, DeclarativeBase):
    __allow_unmapped__ = True
    id: uuid.UUID


PrimaryKeyColumn = Column(UUID, primary_key=True, default=next_id)
