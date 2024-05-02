from collections.abc import Iterator, Generator
from contextlib import contextmanager
from typing import Any, TypeVar

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import Mapper, DeclarativeBase

T = TypeVar("T")


class ModelBase:
    __table__: Any
    awaitable_attrs: Any
    registry: Any

    def update(self, **kw) -> None:
        for key, value in kw.items():
            setattr(self, key, value)

    @classmethod
    def map_imperatively(
        cls,
        class_: type[T],
        model: type[DeclarativeBase],
        **kw: Any,
    ) -> Mapper[T]:
        return cls.registry.map_imperatively(class_, model.__table__, **kw)

    @classmethod
    def get_fields(cls) -> Iterator[str]:
        return (field.name for field in sa.inspect(cls).c)  # type: ignore

    def as_dict(self) -> dict:
        return {key: getattr(self, key) for key in self.get_fields()}

    def __repr__(self) -> str:
        column_data = ", ".join(
            f"{col.name}={getattr(self, col.name)}"
            for col in self.__table__.columns  # type: ignore
        )
        rels_data = ", ".join(
            f"{key}={getattr(self, key)}"
            for key in self.__mapper__.relationships.keys()  # type: ignore
        )
        rels_data = ", " + rels_data if rels_data else ""
        return f"{type(self).__name__}({column_data}{rels_data})"


@contextmanager
def suppress_echo(engine: AsyncEngine) -> Generator:
    engine.echo = False
    yield
    engine.echo = True
