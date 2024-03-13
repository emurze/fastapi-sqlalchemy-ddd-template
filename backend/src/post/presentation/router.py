from fastapi import APIRouter
from fastapi_cache.decorator import cache
from starlette import status
from starlette.responses import JSONResponse

from post.application.command import CreatePostCommand
from post.application.command.delete_post import DeletePostCommand
from post.application.command.update_post import UpdatePostCommand
from post.application.query.get_post import GetPostQuery
from post.presentation import schema as s
from shared.application.dtos import FailedOutputDto
from shared.presentation.dependencies import BusDep
from shared.presentation.json_dtos import FailedJsonResponse
from shared.presentation.utils import raise_errors

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get(
    "/{post_id}",
    status_code=status.HTTP_200_OK,
    response_model=s.PostResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {'model': FailedJsonResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': FailedJsonResponse},
    }
)
@cache(expire=15)
async def get_post(post_id: int, bus: BusDep):
    query = GetPostQuery(id=post_id)
    output_dto = raise_errors(await bus.handle(query))
    return output_dto


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=s.PostResponse,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': FailedJsonResponse},
    }
)
async def create_post(dto: s.CreatePostJsonRequest, bus: BusDep):
    command = CreatePostCommand.model_validate(dto)
    created_output_dto = raise_errors(await bus.handle(command))

    query = GetPostQuery(id=created_output_dto.id)
    output_dto = raise_errors(await bus.handle(query))

    return output_dto


@router.delete(
    "/{post_id}",
    response_description="Deleted",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    responses={
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': FailedJsonResponse},
    }
)
async def delete_post(post_id: int, bus: BusDep):
    command = DeletePostCommand(id=post_id)
    raise_errors(await bus.handle(command))


@router.put(
    "/{post_id}",
    response_description="Updated",
    status_code=status.HTTP_200_OK,
    response_model=s.PostResponse,
    responses={
        status.HTTP_201_CREATED: {'model': s.PostResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': FailedJsonResponse},
    }
)
async def update_post(post_id: int, dto: s.PostResponse, bus: BusDep):
    command = UpdatePostCommand(**(dto.model_dump() | {"id": post_id}))
    output_dto = await bus.handle(command)

    if not output_dto.status:
        if output_dto.message == FailedOutputDto.RESOURCE_NOT_FOUND_ERROR:
            command = CreatePostCommand(**(dto.model_dump() | {"id": post_id}))
            raise_errors(await bus.handle(command))

            query = GetPostQuery(id=post_id)
            get_output_dto = raise_errors(await bus.handle(query))

            return JSONResponse(
                s.PostResponse.model_validate(
                    get_output_dto
                ).model_dump(),
                status.HTTP_201_CREATED,
            )

        return FailedJsonResponse.build_by_output_dto(output_dto)

    query = GetPostQuery(id=post_id)
    get_output_dto = raise_errors(await bus.handle(query))
    return get_output_dto
