import pytest

from tests.seedwork.confdata.domain.entities import Example
from tests.seedwork.confdata.infra.uow import ITestUnitOfWork


@pytest.mark.integration
async def test_uow_can_commit(uow: ITestUnitOfWork) -> None:
    async with uow:
        await uow.examples.add(Example(name="Hello"))
        await uow.commit()

    async with uow:
        example = await uow.examples.get_by_id(1)
        assert example.name == "Hello"


@pytest.mark.integration
async def test_uow_can_rollback(uow: ITestUnitOfWork) -> None:
    async with uow:
        await uow.examples.add(Example(name="Hello"))
        await uow.commit()

    async with uow:
        example = await uow.examples.get_by_id(1)
        assert example.name == "Hello"


@pytest.mark.integration
async def test_uow_can_commit_commit_rollback_rollback_commit(
    uow: ITestUnitOfWork,
) -> None:
    # COMMIT
    async with uow:
        await uow.examples.add(Example(name="Hello 1"))
        await uow.commit()

    # COMMIT
    async with uow:
        await uow.examples.add(Example(name="Hello 2"))
        await uow.commit()

    # ROLLBACK
    async with uow:
        await uow.examples.add(Example(name="Hello"))

    # ROLLBACK
    async with uow:
        await uow.examples.add(Example(name="Hello"))
        await uow.rollback()

    # COMMIT
    async with uow:
        await uow.examples.add(Example(name="Hello 3"))
        await uow.commit()

    # await session.execute(select())
    #
    # example = await uow.examples.get_by_id(1)
    # assert example.name == "Hello"
