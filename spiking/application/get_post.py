from dataclasses import asdict
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from seedwork.application.queries import Query
from seedwork.domain.errors import Error
from spiking.domain.entities import Post


class GetPostQuery(Query):
    id: UUID


async def get_post(query: GetPostQuery, session: AsyncSession) -> dict | Error:
    _query = (
        select(Post)
        .filter_by(id=query.id)
        .options(selectinload(Post.authors))  # type: ignore
    )
    result = await session.execute(_query)
    example = result.scalar_one_or_none()

    if example is None:
        return Error.not_found()

    return asdict(example)
