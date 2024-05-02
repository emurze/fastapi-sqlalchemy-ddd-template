from uuid import UUID

from seedwork.application.commands import Command
from seedwork.application.dtos import DTO
from seedwork.domain.errors import Error
from tests.seedwork.confdata.domain.entities import Example
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
