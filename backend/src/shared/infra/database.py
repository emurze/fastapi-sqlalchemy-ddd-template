import uuid

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped

from seedwork.infra.database import ModelBase


class Model(ModelBase, AsyncAttrs, DeclarativeBase):
    __allow_unmapped__ = True
    id: Mapped[uuid.UUID]
