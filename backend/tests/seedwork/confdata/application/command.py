from uuid import UUID

from pydantic import ValidationError

from seedwork.application.commands import Command, CommandResult
from seedwork.application.dtos import DTO
from seedwork.domain.errors import Error
from seedwork.domain.structs import alist
from tests.seedwork.confdata.domain.entities import Example, ExampleItem
from tests.seedwork.confdata.domain.ports import ITestUnitOfWork
from tests.seedwork.domain.test_value_objects import Address


class AddressDTO(DTO):
    id: UUID
    city: str


class ExampleItemDTO(DTO):
    id: UUID
    name: str
    addresses: list[AddressDTO] = []


class CreateExampleCommand(Command):
    id: UUID
    name: str
    items: list[ExampleItemDTO] = []


async def create_example(
    command: CreateExampleCommand,
    uow: ITestUnitOfWork,
) -> CommandResult:
    async with uow:
        try:
            example = Example(
                **command.model_dump(exclude={"items"}),
                items=alist(
                    [
                        ExampleItem(
                            **item.model_dump(exclude={"addresses"}),
                            addresses=alist(
                                [
                                    Address(**addr.model_dump())
                                    for addr in item.addresses
                                ]
                            ),
                        )
                        for item in command.items
                    ]
                ),
            )
            uow.examples.add(example)
        except ValidationError as e:
            return CommandResult(errors=Error.validation(e.errors()))
        await uow.commit()
        return CommandResult(payload={"id": command.id})


class UpdateExampleCommand(Command):
    id: UUID
    name: str
    items: list[ExampleItemDTO] = []


async def update_example(
    command: UpdateExampleCommand,
    uow: ITestUnitOfWork,
):
    async with uow:
        example = await uow.examples.get_by_id(command.id)
        try:
            example.update(
                **command.model_dump(exclude={"id", "items"}),
                items=alist(
                    [
                        ExampleItem(
                            **item.model_dump(exclude={"addresses"}),
                            addresses=alist(
                                [
                                    Address(**addr.model_dump())
                                    for addr in item.addresses
                                ]
                            ),
                        )
                        for item in command.items
                    ]
                ),
            )
        except ValidationError as e:
            print(f"{e=}")
            return CommandResult(errors=Error.validation(e.errors()))
        await uow.commit()
        return CommandResult()


class DeleteExampleCommand(Command):
    id: UUID


async def delete_example(command: DeleteExampleCommand, uow: ITestUnitOfWork):
    async with uow:
        await uow.examples.delete_by_id(command.id)
        await uow.commit()
        return CommandResult()
