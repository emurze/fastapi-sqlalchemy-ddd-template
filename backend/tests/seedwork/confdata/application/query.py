from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.application.queries import Query, QueryResult
from seedwork.domain.errors import Error
from tests.seedwork.confdata.infra.models import ExampleModel


class GetExampleQuery(Query):
    id: UUID


async def get_example(
    query: GetExampleQuery,
    session: AsyncSession,
) -> dict | Error:
    example = await session.get(ExampleModel, query.id)

    if example is None:
        return Error.not_found()

    return example.scalar_one().as_dict()


class GetExamplesQuery(Query):
    pass


async def get_examples(
    query: GetExamplesQuery, session: AsyncSession
) -> QueryResult:
    pass
