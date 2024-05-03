import pytest
from sqlalchemy.exc import MissingGreenlet

from seedwork.domain.repositories import IGenericRepository
from seedwork.domain.services import next_id
from tests.seedwork.confdata.domain.entities import Example
from tests.seedwork.confdata.domain.ports import ITestUnitOfWork


class TestSqlAlchemyRepository:
    @pytest.mark.integration
    async def test_can_add_and_get(self, sql_uow: ITestUnitOfWork) -> None:
        async with sql_uow as uow:
            example = Example(name="example")
            uow.examples.add(example)
            retrieved = await uow.examples.get_by_id(example.id)
            assert retrieved.name == "example"

    @pytest.mark.integration
    async def test_can_delete(self, sql_uow: ITestUnitOfWork) -> None:
        async with sql_uow as uow:
            example = Example(name="example")
            uow.examples.add(example)
            await uow.examples.delete(example)
            res = await uow.examples.get_by_id(example.id)
            assert res is None

    @pytest.mark.integration
    async def test_can_delete_by_id(self, sql_uow: ITestUnitOfWork) -> None:
        async with sql_uow as uow:
            example = Example(name="example")
            uow.examples.add(example)
            await uow.examples.delete_by_id(example.id)
            res = await uow.examples.get_by_id(example.id)
            assert res is None

    @pytest.mark.integration
    async def test_can_get_by_id_not_found_as_none(
        self, sql_uow: ITestUnitOfWork
    ) -> None:
        async with sql_uow as uow:
            res = await uow.examples.get_by_id(next_id())
            assert res is None

    @pytest.mark.integration
    async def test_can_count(self, sql_uow: ITestUnitOfWork) -> None:
        async with sql_uow as uow:
            uow.examples.add(Example(name="example"))
            uow.examples.add(Example(name="example"))
            assert await uow.examples.count() == 2


class TestMemoryRepository:
    sql_repo = TestSqlAlchemyRepository()

    @pytest.mark.unit
    async def test_can_add_and_get(self, mem_uow: ITestUnitOfWork) -> None:
        await self.sql_repo.test_can_add_and_get(mem_uow)

    @pytest.mark.unit
    async def test_can_delete(self, mem_uow: ITestUnitOfWork) -> None:
        await self.sql_repo.test_can_delete(mem_uow)

    @pytest.mark.unit
    async def test_can_delete_by_id(self, mem_uow: ITestUnitOfWork) -> None:
        await self.sql_repo.test_can_delete_by_id(mem_uow)

    @pytest.mark.unit
    async def test_can_get_by_id_not_found_as_none(
        self, mem_uow: ITestUnitOfWork
    ) -> None:
        await self.sql_repo.test_can_get_by_id_not_found_as_none(mem_uow)

    @pytest.mark.unit
    async def test_can_count(self, mem_uow: ITestUnitOfWork) -> None:
        await self.sql_repo.test_can_count(mem_uow)

    @pytest.mark.marked
    @pytest.mark.unit
    async def test_repositories_with_explicit_binding(
        self, mem_examples: IGenericRepository
    ) -> None:
        mem_examples.add(added := Example(name="example"))
        example = await mem_examples.get_by_id(added.id)
        with pytest.raises(MissingGreenlet):
            _ = example.items
