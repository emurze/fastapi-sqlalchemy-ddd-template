from dataclasses import dataclass

from auth.application.queries.get_clients import (
    GetClientsQuery,
    GetClientsResult,
    GetClientsPayload,
)
from auth.domain.uow import IAuthUnitOfWork
from shared.application.query_handler import IQueryHandler


@dataclass(frozen=True, slots=True)
class GetClientsHandler(IQueryHandler):
    uow: IAuthUnitOfWork

    async def execute(self, query: GetClientsQuery) -> GetClientsResult:
        async with self.uow:
            clients = await self.uow.clients.list()
            payload = GetClientsPayload(clients=clients)
            return GetClientsResult(payload=payload)
