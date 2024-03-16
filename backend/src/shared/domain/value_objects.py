from enum import Enum
from typing import Union, TypeAlias, TypeVar


class Deferred(Enum):
    pass


T = TypeVar("T")
deferred: TypeAlias = Union[T, type[Deferred]]
