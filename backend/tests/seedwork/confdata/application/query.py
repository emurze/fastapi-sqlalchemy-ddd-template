from uuid import UUID

from seedwork.application.queries import Query, QueryResult
from seedwork.domain.errors import Error
from tests.seedwork.confdata.domain.ports import ITestUnitOfWork


class GetExampleQuery(Query):
    id: UUID


async def get_example(
    query: GetExampleQuery,
    uow: ITestUnitOfWork,
) -> QueryResult:
    async with uow:
        example = await uow.query_examples.get(id=query.id)

        if example is None:
            return QueryResult(error=Error.not_found())

        payload = example.as_dict() | {
            "items": [
                item.as_dict()
                | {"addresses": [addr.as_dict() for addr in item.addresses]}
                for item in example.items
            ]
        }
        return QueryResult(payload=payload)
