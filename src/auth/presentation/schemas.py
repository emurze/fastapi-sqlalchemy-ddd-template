from datetime import datetime
from typing import Optional

from shared.presentation.schema import Schema


class AddClientJsonRequest(Schema):
    username: str


class AddClientJsonResponse(Schema):
    id: int
    username: str
    date_joined: datetime
    last_login: Optional[datetime] = None


class GetClientJsonRequest(Schema):
    client_id: int


class GetClientJsonResponse(Schema):
    id: int
    username: str
    date_joined: datetime
    last_login: Optional[datetime] = None
