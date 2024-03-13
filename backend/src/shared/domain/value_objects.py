from typing import Union, TypeAlias, TypeVar


class _Metadata:
    def __init__(self, *args, **kw) -> None:
        pass


T = TypeVar("T")
lazy: TypeAlias = Union[T, _Metadata]
metadata: TypeAlias = _Metadata
