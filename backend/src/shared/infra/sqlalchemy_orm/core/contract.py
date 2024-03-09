from collections.abc import Callable
from dataclasses import dataclass
from typing import Optional, Any as MetaData


@dataclass(frozen=True, slots=True)
class DBContract:
    metadata: Optional[MetaData] = None
    mapper_runner: Optional[Callable] = None
