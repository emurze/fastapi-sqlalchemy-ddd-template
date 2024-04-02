from auth.application.query.get_accounts import GetAccountsQuery
from seedwork.application.messagebus import MessageBus


async def test_get_accounts(bus: MessageBus) -> None:
    query = GetAccountsQuery()
    res = await bus.handle(query)
    assert res  # todo: extend
