import pytest
from httpx import AsyncClient


@pytest.mark.e2e
async def test_health_check(ac: AsyncClient) -> None:
    response = await ac.get("/health")
    assert response.json() == {"message": "I'm healthy!"}
