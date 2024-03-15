from dataclasses import dataclass, field
from typing import Any, Optional

from shared.application.utils import DataclassMixin


class Query(DataclassMixin):
    pass


@dataclass
class QueryResult(DataclassMixin):
    payload: Any = None
    events: list = field(default_factory=list)
    error: Optional[str] = None
