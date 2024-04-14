import pytest

from seedwork.domain.services import next_id
from tests.seedwork.confdata.domain import Example
from tests.seedwork.confdata.ports import IExampleRepository


class TestMemoryRepository:
    @pytest.mark.unit
    async def test_add_and_get_example(
        self, mem_repo: IExampleRepository
    ) -> None:
        example = Example(name="example")
        await mem_repo.add(example)
        retrieved = await mem_repo.get_by_id(example.id)
        assert retrieved.name == "example"

    @pytest.mark.unit
    async def test_delete(self, mem_repo: IExampleRepository) -> None:
        example = Example(name="example")
        await mem_repo.add(example)
        await mem_repo.delete(example)
        res = await mem_repo.get_by_id(example.id)
        assert res is None

    @pytest.mark.unit
    async def test_delete_by_id(self, mem_repo: IExampleRepository) -> None:
        example = Example(name="example")
        await mem_repo.add(example)
        await mem_repo.delete_by_id(example.id)
        res = await mem_repo.get_by_id(example.id)
        assert res is None

    @pytest.mark.unit
    async def test_get_by_id_not_found_returns_none(
        self, mem_repo: IExampleRepository
    ) -> None:
        res = await mem_repo.get_by_id(next_id())
        assert res is None


class TestSqlAlchemyRepository:
    mem_tests = TestMemoryRepository()

    @pytest.mark.integration
    async def test_add_update_example(
        self, sql_repo: IExampleRepository
    ) -> None:
        await self.mem_tests.test_add_and_get_example(sql_repo)

    @pytest.mark.integration
    async def test_delete(self, sql_repo: IExampleRepository) -> None:
        await self.mem_tests.test_delete(sql_repo)

    @pytest.mark.integration
    async def test_delete_by_id(self, sql_repo: IExampleRepository) -> None:
        await self.mem_tests.test_delete_by_id(sql_repo)

    @pytest.mark.integration
    async def test_get_by_id_not_found_returns_none(
        self, sql_repo: IExampleRepository
    ) -> None:
        await self.mem_tests.test_get_by_id_not_found_returns_none(sql_repo)
