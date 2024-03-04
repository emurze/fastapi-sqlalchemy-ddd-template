from typing import Annotated, Any

from fastapi import Depends


def to_params(obj: Any) -> Any:
    return Annotated[obj, Depends()]
