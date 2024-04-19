from typing import TypeVar, Annotated

from pydantic import BaseModel, ConfigDict, AfterValidator

from seedwork.domain.structs import alist

T = TypeVar('T')
V = TypeVar('V')


class DTO(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


def _to_alist(v: list[T]) -> alist[T]:
    if not isinstance(v, list):
        raise ValueError("Expected a list")
    return alist(v)


to_alist = Annotated[V, AfterValidator(_to_alist)]
