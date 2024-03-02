from auth.application.query.get_client import GetClientHandler, GetClientQuery
from auth.domain.uow import IAuthUnitOfWork
from tests.unit.auth.handlers.conftest import make_client


async def test_get_client_handler(uow: IAuthUnitOfWork) -> None:
    await make_client(uow, username="Vlad")

    handler = GetClientHandler(uow)
    query = GetClientQuery(id=1)
    result = await handler.execute(query)
    assert result.id == 1
