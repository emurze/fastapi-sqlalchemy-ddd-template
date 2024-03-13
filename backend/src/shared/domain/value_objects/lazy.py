from typing import Union, TypeAlias


class _Metadata:
    def __init__(self, *args, **kw) -> None:
        pass


class _Lazy:
    def __class_getitem__(cls, item: type):
        return Union[item, _Metadata]


lazy: TypeAlias = _Lazy
metadata: TypeAlias = _Metadata
