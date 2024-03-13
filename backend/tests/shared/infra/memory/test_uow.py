import pytest

from tests.shared.conftest_data.domain import IExampleUnitOfWork, Example


@pytest.mark.unit
async def test_can_rollback(uow: IExampleUnitOfWork) -> None:
    async with uow:
        await uow.examples.add(Example(name="example"))

    async with uow:
        examples = await uow.examples.list()
        assert len(examples) == 0


@pytest.mark.unit
async def test_can_commit(uow: IExampleUnitOfWork) -> None:
    async with uow:
        await uow.examples.add(Example(name="example"))
        await uow.commit()

    async with uow:
        examples = await uow.examples.list()

        assert len(examples) == 1
        assert examples[0].id == 1
        assert examples[0].name == "example 1"


@pytest.mark.unit
async def test_can_commit_rollback_rollback_commit_commit_rollback(
    uow: IExampleUnitOfWork,
) -> None:
    # COMMIT
    async with uow:
        await uow.examples.add(Example(name="example"))
        await uow.commit()

    # ROLLBACK
    async with uow:
        await uow.examples.add(Example(name="example"))
        await uow.examples.add(Example(name="example"))

    # ROLLBACK
    async with uow:
        await uow.examples.add(Example(name="example"))

    # COMMIT
    async with uow:
        await uow.examples.add(Example(name="example"))
        await uow.examples.add(Example(name="example"))
        await uow.commit()

    # COMMIT
    async with uow:
        await uow.examples.add(Example(name="example"))
        await uow.commit()

    # ROLLBACK
    async with uow:
        await uow.examples.add(Example(name="example"))

    # ASSERT
    async with uow:
        examples = await uow.examples.list()
        assert len(examples) == 4
