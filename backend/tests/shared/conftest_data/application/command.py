from dataclasses import dataclass
from typing import Optional, Union

from shared.application.commands import ICommandHandler, Command
from shared.application.dtos import SuccessOutputDto, FailedOutputDto
from tests.shared.conftest_data.domain import IExampleUnitOfWork

CreateExampleOrF = Union["CreateExampleOutputDto", FailedOutputDto]


class CreateExampleCommand(Command):
    id: Optional[int] = None
    name: str


class CreateExampleOutputDto(SuccessOutputDto):
    id: int


@dataclass(frozen=True, slots=True)
class CreateExampleHandler(ICommandHandler):
    uow: IExampleUnitOfWork

    async def handle(self, command: CreateExampleCommand) -> CreateExampleOrF:
        try:
            client_dict = command.model_dump(exclude_none=True)
            async with self.uow:
                client_id = await self.uow.examples.create(**client_dict)
                await self.uow.commit()
                return CreateExampleOutputDto(id=client_id)
        except SystemError:
            return FailedOutputDto.build_system_error()
