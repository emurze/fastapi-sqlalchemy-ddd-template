import pytest
from httpx import AsyncClient
from starlette import status

from tests.blog.presentation.conftest import create_post


@pytest.mark.e2e
async def test_update_post_when_it_doesnt_exist(ac: AsyncClient) -> None:
    response_update = await ac.put(
        "/posts/1", json={"title": "Vlados", "content": "Hello"}
    )
    assert response_update.status_code == status.HTTP_201_CREATED

    # response = await ac.get("/posts/1")
    # assert response.status_code == status.HTTP_200_OK
    # assert response.json() == {
    #     "id": 1,
    #     "title": "Vlados",
    #     "content": "Hello",
    #     "draft": False,
    # }


@pytest.mark.e2e
async def test_update_post_when_it_already_exists(ac: AsyncClient) -> None:
    response_create = await create_post(ac, title="Vlad", content="Hello")
    assert response_create.status_code == status.HTTP_201_CREATED

    response_update = await ac.put(
        "/posts/1", json={"title": "Vlad", "content": "Hello"}
    )
    assert response_update.status_code == status.HTTP_200_OK
    #
    # response = await ac.get("/posts/1")
    # assert response.status_code == status.HTTP_200_OK
    #
    # post = response.json()
    # assert post["id"] == 1
    # assert post["title"] == "Vlad"
    # assert post["content"] == "Hello"
