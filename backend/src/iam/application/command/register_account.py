from uuid import UUID

from pydantic import ValidationError, Field

from iam.domain.entities import Account
from seedwork.application.commands import Command, CommandResult
from seedwork.domain.errors import Error
from seedwork.domain.services import next_id
from shared.domain.uow import IUnitOfWork


class RegisterAccountCommand(Command):
    id: UUID = Field(default_factory=next_id)
    name: str


async def register_account_handler(
    command: RegisterAccountCommand,
    uow: IUnitOfWork,
) -> CommandResult:
    async with uow:
        try:
            await uow.accounts.add(Account.model_validate(command))
        except ValidationError as e:
            return CommandResult(error=Error.validation(e.errors()))

        await uow.commit()
        return CommandResult(payload={"id": command.id})
