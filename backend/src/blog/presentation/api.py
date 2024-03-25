import logging

from fastapi import APIRouter
from starlette import status

from blog.application.command import CreatePostCommand
from blog.application.command.delete_post import DeletePostCommand
from blog.application.command.update_post import UpdatePostCommand
from blog.presentation import schema as s
from seedwork.domain.errors import ErrorType
from seedwork.presentation.json_dtos import FailedJsonResponse
from seedwork.presentation.utils import handle_errors, Response
from seedwork.presentation.dependencies import BusDep

lg = logging.getLogger(__name__)
router = APIRouter(prefix="/posts", tags=["posts"])

# @router.get(
#     "/{post_id}",
#     status_code=status.HTTP_200_OK,
#     response_model=s.PostResponse,
#     responses={
#         status.HTTP_404_NOT_FOUND: {"model": FailedJsonResponse},
#         status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": FailedJsonResponse},
#     },
# )
# @cache(expire=15)
# async def get_post(post_id: int, bus: BusDep):
#     lg.info('Running get post')
#     query = GetPostQuery(id=post_id)
#     query_result = await bus.handle(query)
#     handle_errors(query_result, [ErrorType.NOT_FOUND])
#     return query_result.payload


@router.post(
    "/",
    response_description="Successfully Created",
    status_code=status.HTTP_201_CREATED,
    response_model=s.CreatePostResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": FailedJsonResponse},
    },
)
async def create_post(dto: s.PostRequest, bus: BusDep):
    lg.info('Running create post')
    command = CreatePostCommand(**dto.model_dump())
    create_result = await bus.handle(command)
    handle_errors(create_result, [ErrorType.VALIDATION, ErrorType.CONFLICT])
    return create_result.payload


@router.delete(
    "/{post_id}",
    response_description="Successfully Deleted",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": FailedJsonResponse},
    },
)
async def delete_post(post_id: int, bus: BusDep):
    lg.info('Running delete post')
    command = DeletePostCommand(id=post_id)
    await bus.handle(command)


@router.put(
    "/{post_id}",
    response_description="Successfully Updated",
    status_code=status.HTTP_200_OK,
    response_model=s.CreatePostResponse,
    responses={
        status.HTTP_201_CREATED: {
            "model": s.CreatePostResponse,
            "description": "Successfully Created",
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": FailedJsonResponse},
    },
)
async def update_post(post_id: int, dto: s.PostRequest, bus: BusDep):
    lg.info('Running update post')
    full_dto_dict = dto.model_dump() | {"id": post_id}
    command = UpdatePostCommand(**full_dto_dict)
    update_result = await bus.handle(command)

    if update_result.error.type == ErrorType.NOT_FOUND:
        command = CreatePostCommand(**full_dto_dict)
        result = await bus.handle(command)
        status_code = status.HTTP_201_CREATED
        return Response(result.payload, s.CreatePostResponse, status_code)

    handle_errors(update_result, [ErrorType.VALIDATION])
    return {"id": post_id}
