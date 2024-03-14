from dataclasses import dataclass, field
from typing import Any

from shared.application.dtos import Model


class Command(Model):
    pass


@dataclass(kw_only=True)
class CommandResult:
    payload: Any = None
    errors: list = field(default_factory=list)
    events: list = field(default_factory=list)
