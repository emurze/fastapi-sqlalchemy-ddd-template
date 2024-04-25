import pytest

from seedwork.domain.services import next_id
from tests.seedwork.confdata.domain.entities import Example
from tests.seedwork.confdata.domain.ports import ITestUnitOfWork


class TestMemoryCommandRepository:
    @pytest.mark.unit
    async def test_add_and_get(self, mem_uow: ITestUnitOfWork) -> None:
        async with mem_uow:
            example = Example(name="example")
            mem_uow.examples.add(example)
            retrieved = await mem_uow.examples.get_by_id(example.id)
            assert retrieved.name == "example"

    @pytest.mark.unit
    async def test_delete(self, mem_uow: ITestUnitOfWork) -> None:
        async with mem_uow:
            example = Example(name="example")
            mem_uow.examples.add(example)
            await mem_uow.examples.delete(example)
            res = await mem_uow.examples.get_by_id(example.id)
            assert res is None

    @pytest.mark.unit
    async def test_delete_by_id(self, mem_uow: ITestUnitOfWork) -> None:
        async with mem_uow:
            example = Example(name="example")
            mem_uow.examples.add(example)
            await mem_uow.examples.delete_by_id(example.id)
            res = await mem_uow.examples.get_by_id(example.id)
            assert res is None

    @pytest.mark.unit
    async def test_get_by_id_not_found_as_none(
        self, mem_uow: ITestUnitOfWork
    ) -> None:
        async with mem_uow:
            res = await mem_uow.examples.get_by_id(next_id())
            assert res is None


class TestSqlAlchemyCommandRepository:
    mem_tests = TestMemoryCommandRepository()

    @pytest.mark.integration
    async def test_add_and_get(self, sql_uow: ITestUnitOfWork) -> None:
        await self.mem_tests.test_add_and_get(sql_uow)

    @pytest.mark.integration
    async def test_delete(self, sql_uow: ITestUnitOfWork) -> None:
        await self.mem_tests.test_delete(sql_uow)

    @pytest.mark.integration
    async def test_delete_by_id(self, sql_uow: ITestUnitOfWork) -> None:
        await self.mem_tests.test_delete_by_id(sql_uow)

    @pytest.mark.integration
    async def test_get_by_id_not_found_as_none(
        self, sql_uow: ITestUnitOfWork
    ) -> None:
        await self.mem_tests.test_get_by_id_not_found_as_none(sql_uow)
