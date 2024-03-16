# from dataclasses import dataclass
# from typing import Union
#
# from shared.application.dtos import SuccessOutputDto, FailedOutputDto
# from shared.application.queries import Query
# from shared.domain.errors import ResourceNotFoundException
# from tests.shared.conftest_data.domain import IExampleUnitOfWork
#
# GetExampleOrFail = Union["GetExampleOutputDto", FailedOutputDto]
#
#
# class GetExampleQuery(Query):
#     id: int
#
#
# class GetExampleOutputDto(SuccessOutputDto):
#     id: int
#     name: str
#
#
# async def get_example_handle(
#     self, query: GetExampleQuery, uow: IExampleUnitOfWork
# ) -> GetExampleOrFail:
#     try:
#         async with self.uow:
#             post = await self.uow.examples.get(**query.model_dump())
#             return GetExampleOutputDto.model_validate(post)
#
#     except ResourceNotFoundException:
#         return FailedOutputDto.build_resource_not_found_error()
#
#     except SystemError:
#         return FailedOutputDto.build_system_error()
