from dataclasses import dataclass

from auth.application.queries.get_client import (
    GetClientQuery,
    GetClientResult,
    GetClientPayload,
)
from auth.domain.uow import IAuthUnitOfWork
from shared.application.query_handler import IQueryHandler


@dataclass(frozen=True, slots=True)
class GetClientHandler(IQueryHandler):
    uow: IAuthUnitOfWork

    async def execute(self, query: GetClientQuery) -> GetClientResult:
        query_dict = query.model_dump()
        async with self.uow:
            client = await self.uow.clients.get(**query_dict)
            payload = GetClientPayload.model_validate(client)
            return GetClientResult(payload=payload)
