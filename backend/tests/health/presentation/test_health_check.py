import pytest
from starlette.testclient import TestClient


@pytest.mark.e2e
def test_health_check(client: TestClient) -> None:
    response = client.get('/health')
    assert response.json() == {"message": "I'm healthy!"}
