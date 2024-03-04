import httpx
from starlette.testclient import TestClient


def test_add_client(client: TestClient) -> None:
    response: httpx.Response = client.post(
        "/clients/", json={"username": "Vlad"}
    )
    response_client = response.json()

    assert response.status_code == 201
    assert response_client["id"] == 1
    assert response_client["username"] == "Vlad"
