from fastapi import APIRouter
from starlette import status
from starlette.responses import JSONResponse

from post.application.command import CreatePostCommand
from post.application.command.delete_post import DeletePostCommand
from post.application.command.update_post import UpdatePostCommand
from post.application.query.get_post import GetPostQuery
from post.presentation import schema as s
from shared.application import errors
from shared.presentation.dependencies import BusDep
from shared.presentation.errors import raise_errors
from shared.presentation.schema import Failed

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=s.GetPostJsonResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {'model': Failed},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': Failed},
    }
)
async def get_post(post_id: int, bus: BusDep):
    query = GetPostQuery(id=post_id)
    result = await bus.handle_query(query, raise_errors=True)
    return result.payload


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=s.CreatePostJsonResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': Failed},
    }
)
async def create_post(dto: s.CreatePostJsonRequest, bus: BusDep):
    command = CreatePostCommand.model_validate(dto)
    created_result = await bus.handle_command(command, raise_errors=True)

    query = GetPostQuery(id=created_result.payload.id)
    result = await bus.handle_query(query, raise_errors=True)

    return s.CreatePostJsonResponse.model_validate(result.payload)


@router.delete(
    "/{post_id}",
    response_description="Deleted",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': Failed},
    }
)
async def delete_post(post_id: int, bus: BusDep):
    command = DeletePostCommand(id=post_id)
    await bus.handle_command(command, raise_errors=True)


@router.put(
    "/{post_id}",
    response_description="Updated",
    status_code=status.HTTP_200_OK,
    response_model=s.UpdatePostJsonResponse,
    responses={
        status.HTTP_201_CREATED: {'model': s.UpdatePostJsonResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': Failed},
    }
)
async def update_post(post_id: int, dto: s.UpdatePostJsonRequest, bus: BusDep):
    command = UpdatePostCommand(**(dto.model_dump() | {"id": post_id}))
    result = await bus.handle_command(command)

    if result.error == errors.RESOURCE_NOT_FOUND_ERROR:
        command = CreatePostCommand(**(dto.model_dump() | {"id": post_id}))
        created_result = await bus.handle_command(command, raise_errors=True)

        query = GetPostQuery(id=created_result.payload.id)
        query_result = await bus.handle_query(query, raise_errors=True)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=s.UpdatePostJsonResponse.model_validate(
                query_result.payload,
            ).model_dump()
        )

    _ = raise_errors(result)

    query = GetPostQuery(id=post_id)
    query_result = await bus.handle_query(query, raise_errors=True)
    return s.UpdatePostJsonResponse.model_validate(query_result.payload)
