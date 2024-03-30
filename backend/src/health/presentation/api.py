import logging

from fastapi import APIRouter
from starlette import status

from health.presentation import schemes as s

lg = logging.getLogger(__name__)
router = APIRouter(prefix="/health", tags=["health"])


@router.get(
    "/",
    response_model=s.HealthResponse,
    status_code=status.HTTP_200_OK,
)
async def check_health():
    lg.info('Running health check')
    return {"message": "I'm healthy!"}
