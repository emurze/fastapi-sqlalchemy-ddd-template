from dataclasses import dataclass, field
from typing import Any

from shared.application.utils import DataclassMixin
from shared.domain.errors import Error, NoneError


class Command(DataclassMixin):
    pass


@dataclass(kw_only=True)
class CommandResult(DataclassMixin):
    payload: Any = None
    events: list = field(default_factory=list)
    error: Error | NoneError = NoneError
