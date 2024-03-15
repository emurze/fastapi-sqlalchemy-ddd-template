from typing import Optional

from shared.application.commands import Command, CommandResult
from tests.shared.conftest_data.domain import IExampleUnitOfWork


class CreateExampleCommand(Command):
    id: Optional[int] = None
    name: str


async def create_example_handler(
    command: CreateExampleCommand, uow: IExampleUnitOfWork
):
    try:
        # client_dict = command.model_dump(exclude_none=True)
        async with uow:
            example_id = await uow.examples.add(**client_dict)
            await uow.commit()
            return CommandResult(payload=example_id)
    except SystemError:
        return CommandResult.build_system_error()
