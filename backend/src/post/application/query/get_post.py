from dataclasses import dataclass

from post.application.query.model_mappers import map_post_model_to_dto
from post.domain.repositories import IPostUnitOfWork
from shared.application.queries import Query, QueryResult
from shared.domain.errors import Error


@dataclass(kw_only=True)
class GetPostQuery(Query):
    id: int


async def get_post_handler(
    query: GetPostQuery,
    uow: IPostUnitOfWork,
) -> QueryResult:
    async with uow:
        post = await uow.posts.get_by_id(query.id)

        if not post:
            return QueryResult(error=Error.NOT_FOUND)

        dto = map_post_model_to_dto(post)
        return QueryResult(payload=dto)
