from fastapi import APIRouter
from fastapi_cache.decorator import cache
from starlette import status

from post.application.command import CreatePostCommand
from post.application.command.delete_post import DeletePostCommand
from post.application.command.update_post import UpdatePostCommand
from post.application.query.get_post import GetPostQuery
from post.presentation import schema as s
from shared.domain.errors import Error
from shared.presentation.dependencies import BusDep
from shared.presentation.json_dtos import FailedJsonResponse
from shared.presentation.utils import handle_errors

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get(
    "/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=s.PostResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": FailedJsonResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": FailedJsonResponse},
    },
)
@cache(expire=15)
async def get_post(post_id: int, bus: BusDep):
    query = GetPostQuery(id=post_id)
    query_result = await bus.handle(query)
    handle_errors(query_result, [Error.NOT_FOUND])
    return query_result.payload


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=int,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": FailedJsonResponse},
    },
)
async def create_post(dto: s.CreatePostJsonRequest, bus: BusDep):
    command = CreatePostCommand(**dto.model_dump())
    create_result = await bus.handle(command)
    return create_result.payload.id


@router.delete(
    "/{post_id}",
    response_description="Deleted",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": FailedJsonResponse},
    },
)
async def delete_post(post_id: int, bus: BusDep):
    command = DeletePostCommand(id=post_id)
    await bus.handle(command)


@router.put(
    "/{post_id}",
    response_description="Updated",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        status.HTTP_201_CREATED: {"model": None},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": FailedJsonResponse},
    },
)
async def update_post(post_id: int, dto: s.PostResponse, bus: BusDep):
    full_dto_dict = dto.model_dump() | {"id": post_id}
    command = UpdatePostCommand(**full_dto_dict)
    update_result = await bus.handle(command)

    if update_result.error == Error.NOT_FOUND:
        command = CreatePostCommand(**full_dto_dict)
        create_result = await bus.handle(command)
        return {"post": create_result.payload.id}
