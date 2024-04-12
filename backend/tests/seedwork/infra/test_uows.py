import pytest

from tests.seedwork.confdata.domain import Example
from tests.seedwork.confdata.ports import ITestUnitOfWork


class TestMemoryUow:
    @pytest.mark.unit
    async def test_uow_can_commit(self, memory_uow: ITestUnitOfWork) -> None:
        async with uow:
            await uow.examples.add(Example(name="Hello"))
            await uow.commit()

        async with uow:
            example = await uow.examples.get_by_id(1)
            assert example.name == "Hello"

    @pytest.mark.unit
    async def test_uow_can_rollback(self, memory_uow: ITestUnitOfWork) -> None:
        async with uow:
            await uow.examples.add(Example(name="Hello"))
            await uow.commit()

        async with uow:
            example = await uow.examples.get_by_id(1)
            assert example.name == "Hello"

    @pytest.mark.unit
    async def test_uow_can_make_commit_rollback_pipeline(
        self, memory_uow: ITestUnitOfWork
    ) -> None:
        async with uow:
            await uow.examples.add(Example(name="Hello 1"))
            await uow.commit()

        async with uow:
            await uow.examples.add(Example(name="Hello 2"))
            await uow.commit()

        async with uow:
            await uow.examples.add(Example(name="Hello"))

        async with uow:
            await uow.examples.add(Example(name="Hello"))
            await uow.rollback()

        async with uow:
            await uow.examples.add(Example(name="Hello 3"))
            await uow.commit()


class TestSqlAlchemyUoW:
    @pytest.mark.integration
    async def test_uow_can_commit(self, sqlalchemy_uow: ITestUnitOfWork) -> None:
        async with uow:
            await uow.examples.add(Example(name="Hello"))
            await uow.commit()

        async with uow:
            example = await uow.examples.get_by_id(1)
            assert example.name == "Hello"

    @pytest.mark.integration
    async def test_uow_can_rollback(self, sqlalchemy_uow: ITestUnitOfWork) -> None:
        async with uow:
            await uow.examples.add(Example(name="Hello"))
            await uow.commit()

        async with uow:
            example = await uow.examples.get_by_id(1)
            assert example.name == "Hello"

    @pytest.mark.integration
    async def test_uow_can_make_commit_rollback_pipeline(
        self, sqlalchemy_uow: ITestUnitOfWork
    ) -> None:
        async with uow:
            await uow.examples.add(Example(name="Hello 1"))
            await uow.commit()

        async with uow:
            await uow.examples.add(Example(name="Hello 2"))
            await uow.commit()

        async with uow:
            await uow.examples.add(Example(name="Hello"))

        async with uow:
            await uow.examples.add(Example(name="Hello"))
            await uow.rollback()

        async with uow:
            await uow.examples.add(Example(name="Hello 3"))
            await uow.commit()
