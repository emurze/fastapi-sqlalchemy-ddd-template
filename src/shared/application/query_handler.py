import abc

from shared.application.queries import Query, QueryResult


class IQueryHandler(abc.ABC):
    @abc.abstractmethod
    async def execute(self, query: Query) -> QueryResult: ...
