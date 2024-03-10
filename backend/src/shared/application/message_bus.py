from shared.application.commands import ICommandHandler, Command
from shared.application.dtos import Result
from shared.application.queries import IQueryHandler, Query


class MessageBus:
    command_handlers: dict[type[Command], ICommandHandler]
    query_handlers: dict[type[Query], IQueryHandler]

    def __init__(self) -> None:
        self.command_handlers = {}
        self.query_handlers = {}

    def register_query_handler(
        self, query: type[Query], handler: IQueryHandler
    ) -> None:
        self.query_handlers[query] = handler

    def register_command_handler(
        self, command: type[Command], handler: ICommandHandler
    ) -> None:
        self.command_handlers[command] = handler

    async def handle_query(self, query: Query) -> Result:
        handler = self.query_handlers[query.__class__]
        return await handler.handle(query)

    async def handle_command(self, command: Command) -> Result:
        handler = self.command_handlers[command.__class__]
        return await handler.handle(command)
