from typing import Optional, TypeVar, Generic, Any

from shared.application.errors import ErrorBuilder
from shared.application.model import Model

T = TypeVar("T")
Command = type("Command", (Model,), {})
CommandPayload = type("Command", (Model,), {})


class CommandResult(ErrorBuilder, Generic[T]):
    payload: Optional[CommandPayload] = None
    error: Optional[str] = None
