# from dataclasses import dataclass
#
# from blog.application.query.model_mappers import map_post_model_to_dto
# from shared.application.queries import Query, QueryResult
# from shared.domain.errors import Error
# from shared.domain.uows import IUnitOfWork
#
#
# @dataclass(kw_only=True)
# class GetPostQuery(Query):
#     id: int
#
#
# async def get_post_handler(
#     query: GetPostQuery,
#     uow: IUnitOfWork,
# ) -> QueryResult:
#     async with uow:
#         post = await uow.posts.get_by_id(query.id)
#
#         if not post:
#             return QueryResult(error=Error.not_found())
#
#         dto = map_post_model_to_dto(post)
#         return QueryResult(payload=dto)
