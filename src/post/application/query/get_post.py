from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from shared.application.queries import Query, QueryPayload, QueryResult
from shared.application.query_handler import IQueryHandler
from shared.domain.exceptions import ResourceNotFoundError
from shared.domain.uow import IGenericUnitOfWork


class GetPostQuery(Query):
    id: int


class GetPostPayload(QueryPayload):
    id: int
    title: str
    content: str
    draft: bool


class GetPostResult(QueryResult[GetPostPayload]):
    pass


@dataclass(frozen=True, slots=True)
class GetPostHandler(IQueryHandler):
    uow: IGenericUnitOfWork

    async def execute(self, query: GetPostQuery) -> GetPostResult:
        try:
            query_dict = query.model_dump()
            async with self.uow:
                post = await self.uow.posts.get(**query_dict)
                payload = GetPostPayload.model_validate(post)
                return GetPostResult(payload=payload)

        except ResourceNotFoundError:
            return GetPostResult.build_resource_not_found_error()

        except SystemError:
            return GetPostResult.build_system_error()
