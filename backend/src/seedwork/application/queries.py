from typing import Any, Optional

from seedwork.application.dtos import DTO
from seedwork.domain.errors import Error


class Query(DTO):
    pass


class QueryResult(DTO):
    payload: Any = None
    error: Optional[Error] = None
