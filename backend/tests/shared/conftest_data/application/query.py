from dataclasses import dataclass
from typing import Union

from shared.application.dtos import SuccessOutputDto, FailedOutputDto
from shared.application.queries import IQueryHandler, Query
from shared.domain.exceptions import ResourceNotFoundException
from tests.shared.conftest_data.domain import IExampleUnitOfWork

GetExampleOrFail = Union['GetExampleOutputDto', FailedOutputDto]


class GetExampleQuery(Query):
    id: int


class GetExampleOutputDto(SuccessOutputDto):
    id: int
    name: str


@dataclass(frozen=True, slots=True)
class GetExampleHandler(IQueryHandler):
    uow: IExampleUnitOfWork

    async def handle(self, query: GetExampleQuery) -> GetExampleOrFail:
        try:
            async with self.uow:
                post = await self.uow.examples.get(**query.model_dump())
                return GetExampleOutputDto.model_validate(post)

        except ResourceNotFoundException:
            return FailedOutputDto.build_resource_not_found_error()

        except SystemError:
            return FailedOutputDto.build_system_error()
