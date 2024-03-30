import pytest
from httpx import AsyncClient
from starlette import status

from tests.blog.presentation.conftest import create_post
#
#
# @pytest.mark.e2e
# async def test_get_post(ac: AsyncClient) -> None:
#     response_create = await create_post(ac, title="Vlad", content="Hello")
#     assert response_create.status_code == status.HTTP_201_CREATED
#
#     response = await ac.get("/posts/1")
#     assert response.status_code == status.HTTP_200_OK
#
#     post = response.json()
#     assert post["id"] == 1
#     assert post["title"] == "Vlad"
#     assert post["content"] == "Hello"
#
#
# @pytest.mark.e2e
# async def test_get_post_not_found_error(ac: AsyncClient) -> None:
#     response = await ac.get("/posts/1")
#     assert response.status_code == status.HTTP_404_NOT_FOUND
