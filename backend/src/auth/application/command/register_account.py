from dataclasses import dataclass

from auth.domain.entities import Account
from seedwork.application.commands import Command, CommandResult
from seedwork.domain.uows import IUnitOfWork


@dataclass(frozen=True, slots=True)
class RegisterAccountCommand(Command):
    name: str


async def register_account_handler(
    command: RegisterAccountCommand,
    uow: IUnitOfWork,
) -> CommandResult:
    async with uow:
        await uow.accounts.add(Account(name=command.name))
