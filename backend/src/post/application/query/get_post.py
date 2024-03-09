from dataclasses import dataclass
from typing import Union

from post.domain.repositories import IPostUnitOfWork
from shared.application.dtos import SuccessResult, FailedResult
from shared.application.queries import IQueryHandler, Query
from shared.domain.exceptions import ResourceNotFoundException

GetPostOrFailedResult = Union['GetPostResult', FailedResult]


class GetPostQuery(Query):
    id: int


class GetPostResult(SuccessResult):
    id: int
    title: str
    content: str
    draft: bool


@dataclass(frozen=True, slots=True)
class GetPostHandler(IQueryHandler):
    uow: IPostUnitOfWork

    async def handle(self, query: GetPostQuery) -> GetPostOrFailedResult:
        try:
            query_dict = query.model_dump()
            async with self.uow:
                post = await self.uow.posts.get(**query_dict)
                return GetPostResult.model_validate(post)

        except ResourceNotFoundException:
            return FailedResult.build_resource_not_found_error()

        except SystemError:
            return FailedResult.build_system_error()
