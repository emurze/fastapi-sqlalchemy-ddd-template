import pytest
from httpx import AsyncClient


@pytest.mark.e2e
async def test_overridden_project_title(ac: AsyncClient) -> None:
    response = await ac.get('/docs')
    assert 'Test' in response.content.decode()
