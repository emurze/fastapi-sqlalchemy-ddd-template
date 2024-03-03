from typing import Optional, Generic, TypeVar

from shared.application.model import Model

Query = type("Query", (Model,), {})
QueryPayload = type("QueryPayload", (Model,), {})

T = TypeVar("T")


class QueryResult(Model, Generic[T]):
    payload: Optional[T] = None
    errors: list = []
