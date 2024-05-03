from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from seedwork.application.dtos import DTO
from seedwork.application.queries import Query
from seedwork.domain.errors import Error
from tests.seedwork.confdata.domain.entities import Example, ExampleItem


class ExampleItemDTO(DTO):
    id: UUID
    name: str


class ExampleDTO(DTO):
    id: UUID
    name: str
    items: list[ExampleItemDTO]


def map_example_to_dto(example: Example) -> dict:
    example = ExampleDTO.model_validate(example)
    return example.model_dump()


class GetExampleQuery(Query):
    id: UUID


async def get_example(
    query: GetExampleQuery,
    session: AsyncSession,
) -> dict | Error:
    res = await session.execute(
        select(Example)
        .options(selectinload(Example.items))  # type: ignore
        .filter_by(id=query.id)
    )
    example = res.scalar_one_or_none()

    if example is None:
        return Error.not_found()

    return map_example_to_dto(example)


class GetExampleItemQuery(Query):
    id: UUID


async def get_example_item(
    query: GetExampleItemQuery,
    session: AsyncSession,
) -> dict | Error:
    res = await session.execute(select(ExampleItem).filter_by(id=query.id))
    example_item = res.scalar_one_or_none()

    if example_item is None:
        return Error.not_found()

    return ExampleItemDTO.model_validate(example_item).model_dump()
