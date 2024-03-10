import httpx
import pytest
from starlette import status
from starlette.testclient import TestClient


@pytest.mark.e2e
def test_delete_post_when_it_exists(client: TestClient) -> None:
    response_create: httpx.Response = client.post(
        "/posts/", json={"title": "Vlad", "content": "Hello World"}
    )
    assert response_create.status_code == status.HTTP_201_CREATED

    response_delete: httpx.Response = client.delete("/posts/1")
    assert response_delete.status_code == status.HTTP_204_NO_CONTENT

    response: httpx.Response = client.get("/posts/1")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.e2e
def test_delete_post_when_it_doesnt_exist_no_err(client: TestClient) -> None:
    response: httpx.Response = client.delete("/posts/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
