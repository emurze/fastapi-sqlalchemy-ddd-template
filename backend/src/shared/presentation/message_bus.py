from shared.application.commands import Command
from shared.application.dtos import Result
from shared.application.message_bus import MessageBus
from shared.application.queries import Query
from shared.presentation.json_dtos import FailedJsonResponse


class ProtectedMessageBus(MessageBus):
    async def handle_query(
        self, query: Query, raise_errors: bool = True
    ) -> Result:
        res = await super().handle_query(query)
        return FailedJsonResponse.raise_errors(res) if raise_errors else res

    async def handle_command(
        self, command: Command, raise_errors: bool = True
    ) -> Result:
        res = await super().handle_command(command)
        return FailedJsonResponse.raise_errors(res) if raise_errors else res
