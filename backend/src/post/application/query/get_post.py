from dataclasses import dataclass
from typing import Union

from post.domain.repositories import IPostUnitOfWork
from shared.application.dtos import SuccessOutputDto, FailedOutputDto
from shared.application.queries import IQueryHandler, Query
from shared.domain.exceptions import ResourceNotFoundException

GetPostOrFailedOutputDto = Union["GetPostOutputDto", FailedOutputDto]


class GetPostQuery(Query):
    id: int


class GetPostOutputDto(SuccessOutputDto):
    id: int
    title: str
    content: str
    draft: bool


@dataclass(frozen=True, slots=True)
class GetPostHandler(IQueryHandler):
    uow: IPostUnitOfWork

    async def handle(self, query: GetPostQuery) -> GetPostOrFailedOutputDto:
        try:
            query_dict = query.model_dump()
            async with self.uow:
                post = await self.uow.posts.get(**query_dict)
                return GetPostOutputDto.model_validate(post)

        except ResourceNotFoundException:
            return FailedOutputDto.build_resource_not_found_error()

        except SystemError:
            return FailedOutputDto.build_system_error()
