from enum import Enum
from typing import Union, TypeAlias, TypeVar

from pydantic import BaseModel, ConfigDict


class Deferred(Enum):
    pass


T = TypeVar("T")
deferred: TypeAlias = Union[type[Deferred], T]


class ValueObject(BaseModel):
    model_config = ConfigDict(frozen=True)
