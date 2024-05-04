import pytest

from tests.seedwork.confdata.domain.entities import Example
from tests.seedwork.confdata.domain.ports import ITestUnitOfWork


class TestSqlAlchemyUnitOfWork:
    @pytest.mark.unit
    async def test_commit(self, sql_uow: ITestUnitOfWork) -> None:
        async with sql_uow as uow:
            example = Example(name="Hello")
            uow.examples.add(example)
            await uow.commit()

        async with sql_uow as uow:
            example = await uow.examples.get_by_id(example.id)
            assert example.name == "Hello"

    @pytest.mark.unit
    async def test_rollback(self, sql_uow: ITestUnitOfWork) -> None:
        async with sql_uow as uow:
            example = Example(name="Hello")
            uow.examples.add(example)
            await uow.rollback()

        async with sql_uow as uow:
            example = await uow.examples.get_by_id(example.id)
            assert example is None

    @pytest.mark.unit
    async def test_commit_rollback_pipeline(
        self, sql_uow: ITestUnitOfWork
    ) -> None:
        async with sql_uow as uow:
            uow.examples.add(Example(name="Hello 1"))
            await uow.commit()

        async with sql_uow as uow:
            uow.examples.add(Example(name="Hello 2"))
            uow.examples.add(Example(name="Hello 3"))
            await uow.commit()

        async with sql_uow as uow:
            uow.examples.add(Example(name="Hello"))

        async with sql_uow as uow:
            uow.examples.add(Example(name="Hello"))
            await uow.rollback()

        async with sql_uow as uow:
            uow.examples.add(Example(name="Hello 4"))
            await uow.commit()

        async with sql_uow as uow:
            assert await uow.examples.count() == 4


class TestMemoryUnitOfWork:
    sql_tests = TestSqlAlchemyUnitOfWork()

    @pytest.mark.integration
    async def test_commit(self, mem_uow: ITestUnitOfWork) -> None:
        await self.sql_tests.test_commit(mem_uow)

    @pytest.mark.integration
    async def test_rollback(self, mem_uow: ITestUnitOfWork) -> None:
        await self.sql_tests.test_rollback(mem_uow)

    @pytest.mark.integration
    async def test_commit_rollback_pipeline(
        self, mem_uow: ITestUnitOfWork
    ) -> None:
        await self.sql_tests.test_commit_rollback_pipeline(mem_uow)
