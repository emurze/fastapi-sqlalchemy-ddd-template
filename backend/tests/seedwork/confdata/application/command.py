from uuid import UUID

from seedwork.application.commands import Command
from seedwork.application.dtos import DTO
from seedwork.domain.errors import Error
from tests.seedwork.confdata.domain.entities import Example, ExampleItem
from tests.seedwork.confdata.domain.ports import ITestUnitOfWork


class ExampleItemDTO(DTO):
    id: UUID
    name: str


class CreateExampleCommand(Command):
    id: UUID
    name: str
    items: list[ExampleItemDTO] = []


async def create_example(
    command: CreateExampleCommand, uow: ITestUnitOfWork
) -> None | Error:
    example, errors = Example.create(**command.model_dump())

    if errors:
        return Error.validation(errors)

    uow.examples.add(example)


class UpdateExampleCommand(Command):
    id: UUID
    name: str


async def update_example(
    command: UpdateExampleCommand, uow: ITestUnitOfWork
) -> None | Error:
    example = await uow.examples.get_by_id(command.id, for_update=True)

    if example is None:
        return Error.not_found()

    await example.awaitable_attrs.items
    errors = example.update(**command.model_dump(exclude={"id", "items"}))

    if errors:
        return Error.validation(errors)


class UpdateExampleItemCommand(Command):
    example_id: UUID
    item_id: UUID
    name: str


async def update_example_item(
    command: UpdateExampleItemCommand, uow: ITestUnitOfWork
) -> None | Error:
    example = await uow.examples.get_by_id(command.example_id, for_update=True)

    if example is None:
        return Error.not_found()

    await example.update_item(command.item_id, name=command.name)


class DeleteExampleCommand(Command):
    id: UUID


async def delete_example(
    command: DeleteExampleCommand, uow: ITestUnitOfWork
) -> None:
    await uow.examples.delete_by_id(command.id)


class DeleteExampleItemCommand(Command):
    example_id: UUID
    item_id: UUID


async def delete_example_item(
    command: DeleteExampleItemCommand, uow: ITestUnitOfWork
) -> None | Error:
    example = await uow.examples.get_by_id(command.example_id, for_update=True)

    if example is None:
        return Error.not_found()


