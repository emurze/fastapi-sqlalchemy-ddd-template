from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from auth.domain.entities import ClientId
from auth.domain.uow import IAuthUnitOfWork
from shared.application.queries import Query, QueryPayload, QueryResult
from shared.application.query_handler import IQueryHandler
from shared.domain.exceptions import ResourceNotFoundError


class GetClientQuery(Query):
    id: ClientId


class GetClientPayload(QueryPayload):
    id: ClientId
    username: str
    date_joined: datetime
    last_login: Optional[datetime] = None


class GetClientResult(QueryResult[GetClientPayload]):
    pass


@dataclass(frozen=True, slots=True)
class GetClientQueryHandler(IQueryHandler):
    uow: IAuthUnitOfWork

    async def execute(self, query: GetClientQuery) -> GetClientResult:
        try:
            query_dict = query.model_dump()
            async with self.uow:
                client = await self.uow.clients.get(**query_dict)
                payload = GetClientPayload.model_validate(client)
                return GetClientResult(payload=payload)

        except ResourceNotFoundError:
            return GetClientResult.build_resource_not_found_error()

        except SystemError:
            return GetClientResult.build_system_error()
