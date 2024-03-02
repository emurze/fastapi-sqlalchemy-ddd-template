from auth.domain.uow import IAuthUnitOfWork
from tests.unit.auth.handlers.conftest import make_client


async def test_add_client_handler(uow: IAuthUnitOfWork) -> None:
    client = await make_client(uow, username="Vlad")
    assert client.id == 1
    assert client.username == "Vlad"
