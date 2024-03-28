import pytest
from httpx import AsyncClient
from starlette import status

from tests.blog.presentation.conftest import create_post


@pytest.mark.e2e
async def test_create_post(ac: AsyncClient) -> None:
    response = await create_post(ac, title="Vlad", content="Hello World")
    assert response.status_code == status.HTTP_201_CREATED

    post = response.json()
    assert len(post) == 1
    assert post["id"] == 1
