from uuid import UUID

from seedwork.application.queries import Query, QueryResult
from seedwork.domain.errors import Error
from tests.seedwork.confdata.ports import ITestUnitOfWork
from tests.seedwork.confdata.repositories import ExampleModel


class GetExampleQuery(Query):
    id: UUID


async def get_example(
    query: GetExampleQuery,
    uow: ITestUnitOfWork,
) -> QueryResult:
    async with uow:
        query_examples

