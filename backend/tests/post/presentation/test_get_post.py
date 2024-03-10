import httpx
import pytest
from starlette import status
from starlette.testclient import TestClient


@pytest.mark.e2e
def test_get_post(client: TestClient) -> None:
    response: httpx.Response = client.post(
        "/posts/", json={
            "title": "Vlad",
            "content": "Hello World"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED

    response: httpx.Response = client.get("/posts/1")
    post = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert post["id"] == 1
    assert post["title"] == "Vlad"
    assert post["content"] == "Hello World"


@pytest.mark.e2e
def test_get_post_not_found_error(client: TestClient) -> None:
    response: httpx.Response = client.get("/posts/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND
