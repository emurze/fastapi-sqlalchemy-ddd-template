from fastapi import APIRouter

router = APIRouter(prefix="/clients", tags=["clients"])


@router.get("/")
async def add_client():
    return 1
