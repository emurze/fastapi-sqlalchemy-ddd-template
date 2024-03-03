import httpx
from starlette.testclient import TestClient


def test_add_client(client: TestClient) -> None:
    response: httpx.Response = client.post(
        "/clients/", json={"username": "Vlad"}
    )
    result = response.json()

    assert response.status_code == 201
    assert result.id == 1
    assert result.username == "Vlad"
