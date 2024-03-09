from typing import Optional, Generic, TypeVar

from shared.application.errors import ErrorBuilder
from shared.application.model import Model

T = TypeVar("T")
Query = type("Query", (Model,), {})
QueryPayload = type("QueryPayload", (Model,), {})


class QueryResult(ErrorBuilder, Generic[T]):
    payload: Optional[T] = None
    error: Optional[str] = None
