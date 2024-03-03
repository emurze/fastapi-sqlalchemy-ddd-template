from auth.application.commands.add_client import (
    AddClientPayload,
    AddClientCommand,
)
from shared.application import commands


class UpdateClientCommand(AddClientCommand):
    id: int


class UpdateClientPayload(AddClientPayload):
    pass


class UpdateClientResult(commands.CommandResult[UpdateClientPayload]):
    pass
