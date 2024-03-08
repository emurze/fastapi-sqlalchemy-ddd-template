from auth.application import auth_module
from auth.application.query.get_client import GetClientPayload
from auth.domain.uow import IAuthUnitOfWork
from shared.application.queries import Query, QueryPayload, QueryResult
from shared.application.query_handler import IQueryHandler


class GetClientsQuery(Query):
    pass


class GetClientsPayload(QueryPayload):
    clients: list[GetClientPayload]


class GetClientsResult(QueryResult[GetClientsPayload]):
    pass


@auth_module.dataclass_query_handler
class GetClientsQueryHandler(IQueryHandler):
    uow: IAuthUnitOfWork

    async def execute(self, query: GetClientsQuery) -> GetClientsResult:
        try:
            async with self.uow:
                clients = await self.uow.clients.list()
                payload = GetClientsPayload(clients=clients)
                return GetClientsResult(payload=payload)
        except SystemError:
            return GetClientsResult.build_system_error()
