from dataclasses import dataclass

from post.application.query.model_mappers import map_post_model_to_dto
from post.domain.repositories import IPostUnitOfWork
from shared.application.queries import Query, QueryResult
from shared.domain.exceptions import ResourceNotFoundException


@dataclass
class GetPostQuery(Query):
    id: int


async def get_post_handler(
    query: GetPostQuery, uow: IPostUnitOfWork
) -> QueryResult:
    try:
        query_dict = query.model_dump()
        async with uow:
            post = await uow.posts.get(**query_dict)
            dto = map_post_model_to_dto(post)
            return QueryResult(payload=dto)

    except ResourceNotFoundException:
        return QueryResult.build_resource_not_found_error()

    except SystemError:
        return QueryResult.build_system_error()
