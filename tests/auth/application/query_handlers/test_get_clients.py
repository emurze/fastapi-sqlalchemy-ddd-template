from auth.application.queries.get_clients import GetClientsQuery
from auth.application.query_handlers.get_clients import GetClientsHandler
from auth.domain.uow import IAuthUnitOfWork
from tests.auth.application.conftest import make_client


async def test_can_get_clients(uow: IAuthUnitOfWork) -> None:
    await make_client(uow, username="Vlad")
    await make_client(uow, username="Vlad")

    handler = GetClientsHandler(uow)
    query = GetClientsQuery()
    result = await handler.execute(query)
    clients = result.payload.clients

    assert len(clients) == 2
