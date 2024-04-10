import asyncio

import pytest
from httpx import AsyncClient
from starlette import status


@pytest.mark.e2e
async def test_account_can_handle_concurrency(ac: AsyncClient) -> None:
    res = await asyncio.gather(
        *(ac.post('/auth/account/', json={"name": "Vlad"}) for _ in range(2))
    )
    assert len(res) == 2
    assert all(r.status_code == status.HTTP_200_OK for r in res)
