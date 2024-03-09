import httpx
import pytest
from starlette.testclient import TestClient


@pytest.mark.e2e
def test_overridden_project_title(client: TestClient) -> None:
    response = client.get('/docs')
    assert 'Test' in response.content.decode()


@pytest.mark.e2e
def test_add_client(client: TestClient) -> None:
    response: httpx.Response = client.post(
        "/posts/", json={
            "title": "Vlad",
            "content": "Hello World"
        }
    )
    response_client = response.json()

    assert response.status_code == 201
    assert response_client["id"] == 1
    assert response_client["title"] == "Vlad"
    assert response_client["content"] == "Hello World"
