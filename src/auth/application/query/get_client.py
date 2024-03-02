from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from auth.domain.entities import ClientId
from auth.domain.uow import IAuthUnitOfWork
from shared.application.queries import IQueryHandler, Query, QueryResult


class GetClientQuery(Query):
    id: ClientId


class GetClientResult(QueryResult):
    id: ClientId
    username: str
    date_joined: datetime
    last_login: Optional[datetime] = None


@dataclass(frozen=True, slots=True)
class GetClientHandler(IQueryHandler):
    uow: IAuthUnitOfWork

    async def execute(self, query: GetClientQuery) -> GetClientResult:
        query_dict = query.model_dump()
        async with self.uow:
            client = await self.uow.clients.get(**query_dict)
            return GetClientResult.model_validate(client)
