from distutils.cmd import Command

from shared.application.command_handler import ICommandHandler
from shared.application.commands import CommandResult
from shared.application.queries import Query, QueryResult
from shared.application.query_handler import IQueryHandler as IQHandler


class MessageBus:
    def __init__(self) -> None:
        self.command_handlers = {}
        self.query_handlers = {}

    def register_query_handler(self, query: Query, handler: IQHandler) -> None:
        self.query_handlers[query] = handler

    def register_command_handler(
        self, command: Command, handler: ICommandHandler
    ) -> None:
        self.command_handlers[command] = handler

    async def handle_query(self, query: Query) -> QueryResult:
        handler = self.query_handlers[type(query)]
        return await handler.execute(query)

    async def handle_command(self, command: Command) -> CommandResult:
        handler = self.command_handlers[type(command)]
        return await handler.execute(command)
