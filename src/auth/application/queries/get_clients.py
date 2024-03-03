from auth.application.queries.get_client import GetClientPayload
from shared.application import queries


class GetClientsQuery(queries.Query):
    pass


class GetClientsPayload(queries.QueryPayload):
    clients: list[GetClientPayload]


class GetClientsResult(queries.QueryResult[GetClientsPayload]):
    pass
