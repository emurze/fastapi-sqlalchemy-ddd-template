from auth.application.queries.get_client import GetClientQuery
from auth.application.query_handlers.get_client import GetClientHandler
from auth.domain.uow import IAuthUnitOfWork
from tests.auth.application.conftest import make_client


async def test_get_client_handler(uow: IAuthUnitOfWork) -> None:
    await make_client(uow, username="Vlad")

    handler = GetClientHandler(uow)
    query = GetClientQuery(id=1)
    result = await handler.execute(query)
    client = result.payload

    assert result.status is True
    assert client.id == 1


async def test_get_client_not_found_error(uow: IAuthUnitOfWork) -> None:
    handler = GetClientHandler(uow)
    query = GetClientQuery(id=1)
    result = await handler.execute(query)
    assert result.status is False
