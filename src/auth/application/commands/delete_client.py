from auth.application.commands.add_client import AddClientPayload
from shared.application import commands


class DeleteClientCommand(commands.Command):
    id: int


class DeleteClientPayload(AddClientPayload):
    pass


class DeleteClientResult(commands.CommandResult[DeleteClientPayload]):
    pass
