from datetime import datetime
from typing import Optional

from auth.domain.entities import ClientId
from shared.application import queries


class GetClientQuery(queries.Query):
    id: ClientId


class GetClientPayload(queries.QueryPayload):
    id: ClientId
    username: str
    date_joined: datetime
    last_login: Optional[datetime] = None


class GetClientResult(queries.QueryResult[GetClientPayload]):
    pass
