import pytest
from starlette.testclient import TestClient


@pytest.mark.e2e
def test_overridden_project_title(client: TestClient) -> None:
    response = client.get('/docs')
    assert 'Test' in response.content.decode()
