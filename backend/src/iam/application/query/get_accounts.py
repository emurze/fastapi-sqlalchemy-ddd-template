from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.application.queries import Query


class GetAccountsQuery(Query):
    pass


async def get_accounts_handler(query: GetAccountsQuery, session: AsyncSession):
    pass
