from typing import Optional, TypeVar, Generic

from shared.application.errors import ErrorBuilder
from shared.application.model import Model

Command = type("Command", (Model,), {})
CommandPayload = type("CommandPayload", (Model,), {})

T = TypeVar("T")


class CommandResult(ErrorBuilder, Generic[T]):
    payload: Optional[T] = None
    error_detail: Optional[str] = None
