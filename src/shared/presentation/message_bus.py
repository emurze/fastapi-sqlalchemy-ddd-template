from shared.application.command_handler import ICommandHandler
from shared.application.commands import CommandResult, Command
from shared.application.message_bus import MessageBus
from shared.application.queries import Query, QueryResult
from shared.application.query_handler import IQueryHandler as IQHandler
from shared.presentation import errors


class ProtectedMessageBus(MessageBus):
    async def handle_query(
        self, query: Query, raise_errors: bool = False
    ) -> QueryResult:
        res = await super().handle_query(query)
        return errors.raise_errors(res) if raise_errors else res

    async def handle_command(
        self, command: Command, raise_errors: bool = False
    ) -> CommandResult:
        res = await super().handle_command(command)
        return errors.raise_errors(res) if raise_errors else res
