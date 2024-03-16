from fastapi import APIRouter
from starlette import status

from health.presentation import schema as s

router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "/",
    response_model=s.HealthResponse,
    status_code=status.HTTP_200_OK,
)
async def health_check():
    return {"message": "I'm healthy!"}
