import pytest

from tests.shared.conftest_data.domain import IExampleUnitOfWork

example_dict = {"name": "example 1"}


@pytest.mark.unit
async def test_can_rollback(uow: IExampleUnitOfWork) -> None:
    async with uow:
        await uow.examples.create(**example_dict)

    async with uow:
        examples = await uow.examples.list()
        assert len(examples) == 0


@pytest.mark.unit
async def test_can_commit(uow: IExampleUnitOfWork) -> None:
    async with uow:
        await uow.examples.create(**example_dict)
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
        await uow.examples.create(**example_dict)
        await uow.commit()

    # ROLLBACK
    async with uow:
        await uow.examples.create(**example_dict)
        await uow.examples.create(**example_dict)

    # ROLLBACK
    async with uow:
        await uow.examples.create(**example_dict)

    # COMMIT
    async with uow:
        await uow.examples.create(**example_dict)
        await uow.examples.create(**example_dict)
        await uow.commit()

    # COMMIT
    async with uow:
        await uow.examples.create(**example_dict)
        await uow.commit()

    # ROLLBACK
    async with uow:
        await uow.examples.create(**example_dict)

    # ASSERT
    async with uow:
        examples = await uow.examples.list()
        assert len(examples) == 4
