import asyncio

import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.e2e
async def test_health(ac: AsyncClient) -> None:
    response = await ac.get("/health/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "I'm healthy!"}


@pytest.mark.e2e
async def test_health_can_handle_several_clients(ac: AsyncClient) -> None:
    res = await asyncio.gather(ac.get("/health/"), ac.get("/health/"))
    assert len(res) == 2
    assert res[0].status_code == status.HTTP_200_OK
    assert res[1].status_code == status.HTTP_200_OK
