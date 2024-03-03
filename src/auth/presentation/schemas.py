from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from shared.presentation.schema import Schema


class AddClientJsonRequest(BaseModel):
    username: str


class AddClientJsonResponse(Schema):
    id: int
    username: str
    date_joined: datetime
    last_login: Optional[datetime] = None
