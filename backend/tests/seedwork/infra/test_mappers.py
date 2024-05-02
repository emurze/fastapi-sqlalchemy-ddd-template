import pytest
from sqlalchemy.exc import MissingGreenlet

from seedwork.domain.services import next_id
from tests.seedwork.confdata.domain.entities import ExampleItem, Example
from tests.seedwork.confdata.domain.ports import ITestUnitOfWork
from tests.seedwork.confdata.infra.models import ExampleModel


class TestModelBaseMixin:
    @pytest.mark.unit
    def test_get_fields_success(self) -> None:
        assert [*ExampleModel.get_fields()] == ["id", "name"]

    @pytest.mark.unit
    def test_as_dict(self) -> None:
        example = ExampleModel(id=(example_id := next_id()), name="Example 1")
        assert example.as_dict() == {"id": example_id, "name": "Example 1"}

    @pytest.mark.skip
    @pytest.mark.unit
    def test_update(self) -> None:
        pass


@pytest.mark.integration
async def test_orm_unloaded_relations_errors(sql_uow: ITestUnitOfWork) -> None:
    async with sql_uow as uow:
        new_example = Example(name="Example", items=[ExampleItem(name="item")])
        uow.examples.add(new_example)
        await uow.commit()

    async with sql_uow as uow:
        example = await uow.examples.get_by_id(new_example.id)
        with pytest.raises(MissingGreenlet):
            _ = example.items

        assert (await example.awaitable_attrs.items)[0].name == "item"
        example.items[0].name = "new item"
        example.items.append(ExampleItem(name="best item"))
        await uow.commit()

    async with sql_uow as uow:
        example = await uow.examples.get_by_id(new_example.id)
        with pytest.raises(MissingGreenlet):
            _ = example.items

        with pytest.raises(MissingGreenlet):
            _ = example.items

        await example.awaitable_attrs.items
        assert example.items[0].name == "new item"
        assert example.items[1].name == "best item"


@pytest.mark.unit
async def test_mem_unloaded_relations_errors(mem_uow: ITestUnitOfWork) -> None:
    await test_orm_unloaded_relations_errors(mem_uow)
