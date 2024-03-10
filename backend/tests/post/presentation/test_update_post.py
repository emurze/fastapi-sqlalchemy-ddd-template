import httpx
import pytest
from starlette import status
from starlette.testclient import TestClient


@pytest.mark.e2e
def test_update_post_when_it_doesnt_exist(client: TestClient) -> None:
    response: httpx.Response = client.put(
        "/posts/1", json={
            "title": "Vlados",
            "content": "Hello"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED

    response: httpx.Response = client.get("/posts/1")
    post = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert post["id"] == 1
    assert post["title"] == "Vlados"
    assert post["content"] == "Hello"


@pytest.mark.e2e
def test_update_post_when_it_already_exists(client: TestClient) -> None:
    response: httpx.Response = client.post(
        "/posts/", json={
            "title": "Vlad",
            "content": "Hello World"
        }
    )
    assert response.status_code == status.HTTP_201_CREATED

    response: httpx.Response = client.put(
        "/posts/1", json={
            "title": "Vladik",
            "content": "Hello"
        }
    )
    assert response.status_code == status.HTTP_200_OK

    response: httpx.Response = client.get("/posts/1")
    post = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert post["id"] == 1
    assert post["title"] == "Vladik"
    assert post["content"] == "Hello"
