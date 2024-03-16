from typing import Union, TypeAlias, TypeVar, NewType

Deferred = NewType("Deferred", None)
T = TypeVar("T")
deferred: TypeAlias = Union[T, Deferred]
