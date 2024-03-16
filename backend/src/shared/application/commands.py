from dataclasses import dataclass, field
from typing import Any, Optional

from shared.application.utils import DataclassMixin
from shared.domain.errors import Error


class Command(DataclassMixin):
    pass


@dataclass(kw_only=True)
class CommandResult(DataclassMixin):
    payload: Any = None
    events: list = field(default_factory=list)
    error: Optional[Error] = None
