import pytest

from auth.domain.uow import IAuthUnitOfWork
from tests.auth.application.conftest import make_client


@pytest.mark.unit
async def test_can_add_client(uow: IAuthUnitOfWork) -> None:
    client = await make_client(uow, username="Vlad")
    assert client.id == 1
    assert client.username == "Vlad"
