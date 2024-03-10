from collections.abc import Iterator

import pytest
from sqlalchemy.orm import clear_mappers

from shared.infra.sqlalchemy_orm.common import suppress_echo
from tests.conftest import engine
from tests.shared.conftest_data.tables import (
    run_example_mappers,
    mapped_registry,
)


@pytest.fixture(scope="function")
def _example_mappers() -> Iterator[None]:
    run_example_mappers()
    yield
    clear_mappers()


@pytest.fixture(scope="function")
async def _restart_example_table(_example_mappers) -> None:
    async with engine.begin() as conn:
        async with suppress_echo(engine):
            await conn.run_sync(mapped_registry.metadata.drop_all)
            await conn.run_sync(mapped_registry.metadata.create_all)
        await conn.commit()
