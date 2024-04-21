from typing import TypeVar

from pydantic import BaseModel, ConfigDict

V = TypeVar('V')


class DTO(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )
