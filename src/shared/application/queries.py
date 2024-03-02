import abc
from pydantic import BaseModel, ConfigDict


class Query(BaseModel):
    pass


class QueryResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class IQueryHandler(abc.ABC):
    @abc.abstractmethod
    async def execute(self, query: Query) -> QueryResult: ...
