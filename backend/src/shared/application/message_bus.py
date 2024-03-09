from distutils.cmd import Command

from shared.application.commands import ICommandHandler
from shared.application.dtos import Result
from shared.application.queries import IQueryHandler as IQHandler, Query


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

    async def handle_query(self, query: Query) -> Result:
        handler = self.query_handlers[type(query)]
        return await handler.handle(query)

    async def handle_command(self, command: Command) -> Result:
        handler = self.command_handlers[type(command)]
        return await handler.handle(command)
