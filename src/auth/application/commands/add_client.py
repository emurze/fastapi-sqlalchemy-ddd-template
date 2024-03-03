from datetime import datetime
from typing import Optional

from auth.domain.entities import ClientId
from shared.application import commands


class AddClientCommand(commands.Command):
    username: str


class AddClientPayload(commands.CommandPayload):
    id: ClientId
    username: str
    date_joined: datetime
    last_login: Optional[datetime] = None


class AddClientResult(commands.CommandResult[AddClientPayload]):
    pass
