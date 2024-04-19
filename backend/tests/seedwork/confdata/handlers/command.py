from uuid import UUID

from pydantic import Field, ValidationError

from seedwork.application.commands import Command, CommandResult
from seedwork.application.dtos import DTO, to_alist
from seedwork.domain.errors import Error
from seedwork.domain.services import next_id
from seedwork.domain.structs import alist
from tests.seedwork.confdata.domain import Example, ExampleItem
from tests.seedwork.confdata.ports import ITestUnitOfWork


class AddressDTO(DTO):
    id: UUID = Field(default_factory=next_id)
    city: str


class ExampleItemDTO(DTO):
    id: UUID = Field(default_factory=next_id)
    name: str
    addresses: to_alist[list[AddressDTO]] = alist()


class CreateExampleCommand(Command):
    id: UUID = Field(default_factory=next_id)
    name: str
    items: to_alist[list[ExampleItemDTO]] = alist()


async def create_example(
    command: CreateExampleCommand,
    uow: ITestUnitOfWork,
) -> CommandResult:
    async with uow:
        try:
            await uow.examples.add(Example.model_validate(command))
        except ValidationError as e:
            return CommandResult(errors=Error.validation(e.errors()))
        await uow.commit()
        return CommandResult(payload={"id": command.id})


class UpdateExampleCommand(Command):
    id: UUID = Field(default_factory=next_id)
    name: str
    items: to_alist[list[ExampleItemDTO]] = alist()


async def update_example(
    command: UpdateExampleCommand,
    uow: ITestUnitOfWork,
) -> CommandResult:
    async with uow:
        example = await uow.examples.get_by_id(command.id)
        example.update(**Example.model_validate(example).model_dump())
        await uow.commit()
        return CommandResult()
