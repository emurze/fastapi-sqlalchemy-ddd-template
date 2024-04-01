from pydantic import ValidationError

from auth.domain.entities import Account
from seedwork.application.commands import Command, CommandResult
from seedwork.application.dtos import DTO
from seedwork.domain.errors import Error
from seedwork.domain.uows import UnitOfWorkFactory


class RegisterAccountCommand(Command):
    name: str


class RegisterAccountPayload(DTO):
    id: int


async def register_account_handler(
    command: RegisterAccountCommand,
    uow_factory: UnitOfWorkFactory,
) -> CommandResult:
    async with uow_factory() as uow:
        try:
            account_id = await uow.accounts.add(Account(name=command.name))
        except ValidationError as e:
            return CommandResult(error=Error.validation(e.errors()))

        await uow.commit()
        return CommandResult(payload=RegisterAccountPayload(id=account_id))
