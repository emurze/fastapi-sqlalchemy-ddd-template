import pytest

from seedwork.domain.services import next_id
from tests.seedwork.confdata.domain import Example
from tests.seedwork.confdata.ports import IExampleRepository


class TestMemoryRepository:
    @pytest.mark.unit
    async def test_add_and_get_example(
        self, memory_repo: IExampleRepository
    ) -> None:
        example = Example(name="example")
        await memory_repo.add(example)
        retrieved = await memory_repo.get_by_id(example.id)
        assert retrieved.name == "example"

    @pytest.mark.unit
    async def test_delete(self, memory_repo: IExampleRepository) -> None:
        example = Example(name="example")
        await memory_repo.add(example)
        await memory_repo.delete(example)
        res = await memory_repo.get_by_id(example.id)
        assert res is None

    @pytest.mark.unit
    async def test_delete_by_id(self, memory_repo: IExampleRepository) -> None:
        example = Example(name="example")
        await memory_repo.add(example)
        await memory_repo.delete_by_id(example.id)
        res = await memory_repo.get_by_id(example.id)
        assert res is None

    @pytest.mark.unit
    async def test_get_by_id_not_found_returns_none(
        self, memory_repo: IExampleRepository
    ) -> None:
        res = await memory_repo.get_by_id(next_id())
        assert res is None


class TestSqlAlchemyRepository:
    mem_tests = TestMemoryRepository()

    @pytest.mark.integration
    async def test_add_update_example(
        self, sqlalchemy_repo: IExampleRepository
    ) -> None:
        await self.mem_tests.test_add_and_get_example(sqlalchemy_repo)

    @pytest.mark.integration
    async def test_delete(self, sqlalchemy_repo: IExampleRepository) -> None:
        await self.mem_tests.test_delete(sqlalchemy_repo)

    @pytest.mark.integration
    async def test_delete_by_id(
        self, sqlalchemy_repo: IExampleRepository
    ) -> None:
        await self.mem_tests.test_delete_by_id(sqlalchemy_repo)

    @pytest.mark.integration
    async def test_get_by_id_not_found_returns_none(
        self, sqlalchemy_repo: IExampleRepository
    ) -> None:
        await self.mem_tests.test_get_by_id_not_found_returns_none(
            sqlalchemy_repo
        )
