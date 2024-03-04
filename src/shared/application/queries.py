from typing import Optional, Generic, TypeVar

from shared.application.errors import ErrorBuilder
from shared.application.model import Model

Query = type("Query", (Model,), {})
QueryPayload = type("QueryPayload", (Model,), {})

T = TypeVar("T")


class QueryResult(ErrorBuilder, Generic[T]):
    payload: Optional[T] = None
    error_detail: Optional[str] = None
