import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.e2e
async def test_health(ac: AsyncClient) -> None:
    response = await ac.get("/health/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "I'm healthy!"}
