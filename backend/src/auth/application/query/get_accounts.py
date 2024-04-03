from select import select

from sqlalchemy.ext.asyncio import AsyncSession

from seedwork.application.queries import Query


class GetAccountsQuery(Query):
    pass


async def get_accounts_handler(query: GetAccountsQuery, session: AsyncSession):
    # Try to implement query builder pattern
    stmt = select()
    await session.execute(stmt)
