import pytest
from httpx import AsyncClient
from starlette import status

from tests.blog.presentation.conftest import create_post


# @pytest.mark.e2e
# async def test_delete_post_when_it_exists(ac: AsyncClient) -> None:
#     response_create = await create_post(ac, title="Vlad", content="Hello")
#     assert response_create.status_code == status.HTTP_201_CREATED
#
#     response_delete = await ac.delete("/posts/1")
#     assert response_delete.status_code == status.HTTP_204_NO_CONTENT
#
#     response = await ac.get("/posts/1")
#     assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.e2e
async def test_delete_post_when_it_doesnt_exist(ac: AsyncClient) -> None:
    response = await ac.delete("/posts/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
