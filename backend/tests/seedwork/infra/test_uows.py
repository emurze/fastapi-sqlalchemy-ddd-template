import pytest
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from seedwork.domain.structs import alist
from tests.seedwork.confdata.domain import Example, ExampleItem
from tests.seedwork.confdata.ports import ITestUnitOfWork
from tests.seedwork.confdata.repositories import ExampleModel, ExampleItemModel


class TestMemoryUnitOfWork:
    @pytest.mark.unit
    async def test_commit(self, mem_uow: ITestUnitOfWork) -> None:
        async with mem_uow as uow:
            example = Example(name="Hello")
            uow.examples.add(example)
            await uow.commit()

        async with mem_uow as uow:
            example = await uow.examples.get_by_id(example.id)
            assert example.name == "Hello"

    @pytest.mark.unit
    async def test_rollback(self, mem_uow: ITestUnitOfWork) -> None:
        async with mem_uow as uow:
            example = Example(name="Hello")
            uow.examples.add(example)
            await uow.rollback()

        async with mem_uow as uow:
            example = await uow.examples.get_by_id(example.id)
            assert example is None

    @pytest.mark.unit
    async def test_commit_rollback_pipeline(
        self, mem_uow: ITestUnitOfWork
    ) -> None:
        async with mem_uow as uow:
            uow.examples.add(Example(name="Hello 1"))
            await uow.commit()

        async with mem_uow as uow:
            uow.examples.add(Example(name="Hello 2"))
            uow.examples.add(Example(name="Hello 3"))
            await uow.commit()

        async with mem_uow as uow:
            uow.examples.add(Example(name="Hello"))

        async with mem_uow as uow:
            uow.examples.add(Example(name="Hello"))
            await uow.rollback()

        async with mem_uow as uow:
            uow.examples.add(Example(name="Hello 4"))
            await uow.commit()

        async with mem_uow as uow:
            assert await uow.examples.count() == 4


class TestSqlAlchemyUnitOfWork:
    mem_tests = TestMemoryUnitOfWork()

    @pytest.mark.integration
    async def test_commit(self, sql_uow: ITestUnitOfWork) -> None:
        await self.mem_tests.test_commit(sql_uow)

    @pytest.mark.integration
    async def test_rollback(self, sql_uow: ITestUnitOfWork) -> None:
        await self.mem_tests.test_rollback(sql_uow)

    @pytest.mark.integration
    async def test_commit_rollback_pipeline(
        self, sql_uow: ITestUnitOfWork
    ) -> None:
        await self.mem_tests.test_commit_rollback_pipeline(sql_uow)


# @pytest.mark.skip(reason="Making mappers")
@pytest.mark.marked
@pytest.mark.integration
async def test_can_update(sql_uow: ITestUnitOfWork) -> None:
    async with sql_uow as uow:
        entity = Example(
            name="Hello",
            items=alist([
                ExampleItem(name="Item A"),
                ExampleItem(name="Item B"),
                ExampleItem(name="Item C"),
                ExampleItem(name="Item D"),
                ExampleItem(name="Item E"),
                ExampleItem(name="Item F"),
                ExampleItem(name="Item G"),
                ExampleItem(name="Item H"),
                ExampleItem(name="Item I"),
                ExampleItem(name="Item J"),
                ExampleItem(name="Item K"),
                ExampleItem(name="Item L"),
                ExampleItem(name="Item M"),
            ])
        )
        uow.examples.add(entity)
        await uow.commit()

    async with sql_uow as uow:
        entity = await uow.examples.get_by_id(entity.id, for_update=True)
        res = await entity.items.just_load()
        print(res)
        await uow.commit()

    # async with sql_uow as uow:
    #     query = select(ExampleModel).options(
    #         selectinload(ExampleModel.items)
    #         .subqueryload(ExampleItemModel.addresses)
    #     )
    #     models = list((await uow.session.execute(query)).scalars())
    #     assert len(models[0].items) == 13
