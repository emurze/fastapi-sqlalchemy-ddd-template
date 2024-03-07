from typing import Optional, TypeVar, Generic

from shared.application.errors import ErrorBuilder
from shared.application.model import Model

T = TypeVar("T")
Command = type("Command", (Model,), {})


class CommandResult(ErrorBuilder, Generic[T]):
    error_detail: Optional[str] = None
