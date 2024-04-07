from enum import Enum
from typing import Union, TypeAlias, TypeVar

from pydantic import BaseModel, ConfigDict


class Deferred(Enum):
    pass


_T = TypeVar("_T")
defer: TypeAlias = Union[type[Deferred], _T]


class ValueObject(BaseModel):
    model_config = ConfigDict(frozen=True)


class Money(ValueObject):
    amount: int = 0
    currency: str = 'USD'
