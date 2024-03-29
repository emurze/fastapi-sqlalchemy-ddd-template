import pytest

from tests.seedwork.confdata.entities import Example
from tests.seedwork.confdata.uow import ISeedWorkUnitOfWork


@pytest.mark.integration
async def test_uow_can_commit(uow: ISeedWorkUnitOfWork) -> None:
    async with uow:
        await uow.examples.add(Example(name="Hello"))
        await uow.commit()

    async with uow:
        example = await uow.examples.get_by_id(1)
        assert example.name == "Hello"


@pytest.mark.integration
async def test_uow_can_rollback(uow: ISeedWorkUnitOfWork) -> None:
    async with uow:
        await uow.examples.add(Example(name="Hello"))
        await uow.commit()

    async with uow:
        example = await uow.examples.get_by_id(1)
        assert example.name == "Hello"
