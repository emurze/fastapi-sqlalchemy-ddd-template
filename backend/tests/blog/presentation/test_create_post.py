import pytest
from httpx import AsyncClient
from starlette import status

from tests.blog.presentation.conftest import create_post


@pytest.mark.e2e
async def test_create_post(ac: AsyncClient) -> None:
    response = await create_post(ac, title="Vlad", content="Hello World")
    assert response.status_code == status.HTTP_201_CREATED

    client = response.json()
    assert client["id"] == 1
    assert client["title"] == "Vlad"
    assert client["content"] == "Hello World"
