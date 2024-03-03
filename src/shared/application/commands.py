from typing import Optional, TypeVar, Generic

from shared.application.model import Model

Command = type("Command", (Model,), {})
CommandPayload = type("CommandPayload", (Model,), {})

T = TypeVar("T")


class CommandResult(Model, Generic[T]):
    payload: Optional[T] = None
    errors: list = []
