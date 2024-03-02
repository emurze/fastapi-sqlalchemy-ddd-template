from collections.abc import Iterable
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncEngine


def combine_metadata(metadata_list: Iterable[MetaData]) -> MetaData:
    combined_metadata = MetaData()

    for metadata in metadata_list:
        for table_name, table in metadata.tables.items():
            combined_metadata._add_table(  # noqa
                table_name, table.schema, table
            )

    return combined_metadata


@asynccontextmanager
async def suppress_echo(engine: AsyncEngine) -> AsyncGenerator:
    engine.echo = False
    yield
    engine.echo = True
