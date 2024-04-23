import pytest

from seedwork.domain.structs import alist
from seedwork.domain.services import next_id
from tests.seedwork.confdata.domain import Example, ExampleItem, Address
from tests.seedwork.confdata.ports import ITestUnitOfWork
from tests.seedwork.confdata.repositories import (
    ExampleMapper,
    ExampleModel,
    ExampleItemModel,
    AddressModel,
)

mapper = ExampleMapper(ExampleModel)


def make_example_model() -> ExampleModel:
    return ExampleModel(
        id=next_id(),
        name='Example1',
        items=[
            ExampleItemModel(
                id=next_id(),
                name='ExampleItem1',
                addresses=[
                    AddressModel(id=next_id(), city='Kiev'),
                ]
            )
        ]
    )


def make_example_entity() -> Example:
    return Example(
        name='Example1',
        items=alist([
            ExampleItem(
                name='ExampleItem1',
                addresses=alist([
                    Address(city='Kiev')
                ])
            )
        ])
    )


@pytest.mark.unit
async def test_model_to_entity() -> None:
    entity = mapper.model_to_entity(make_example_model())
    await entity.items.load()
    await entity.items[0].addresses.load()
    assert entity.name == 'Example1'
    assert entity.items[0].name == 'ExampleItem1'
    assert entity.items[0].addresses[0].city == 'Kiev'


@pytest.mark.unit
def test_can_add_using_entity_with_list_loading() -> None:
    model = mapper.entity_to_model(make_example_entity())
    assert model.name == 'Example1'
    assert model.items[0].name == 'ExampleItem1'
    assert model.items[0].addresses[0].city == 'Kiev'


@pytest.mark.unit
def test_can_update_without_extra_loading() -> None:
    model = make_example_model()
    entity = mapper.model_to_entity(model)
    entity.name = "Vlados"
    mapper.update_model(entity, model)
    assert entity.items.is_loaded() is False
    assert model.name == 'Vlados'
    assert model.items[0].name == 'ExampleItem1'
    assert model.items[0].addresses[0].city == 'Kiev'


@pytest.mark.unit
async def test_can_update_with_loaded_items() -> None:
    model = make_example_model()
    entity = mapper.model_to_entity(model)
    entity.name = "Vlados"
    await entity.items.load()
    await entity.items[0].addresses.load()
    mapper.update_model(entity, model)
    assert entity.items.is_loaded() is True
    assert model.name == 'Vlados'
    assert model.items[0].name == 'ExampleItem1'
    assert model.items[0].addresses[0].city == 'Kiev'


@pytest.mark.marked
@pytest.mark.integration
async def test_repo_and_mapper_can_update(sql_uow: ITestUnitOfWork) -> None:
    async with sql_uow as uow:
        model = Example(
            name="Hello",
            items=alist([
                ExampleItem(
                    name="Item A",
                    addresses=alist([
                        Address(city="Lersk")
                    ]),
                )
                for _ in range(2)
            ])
        )
        uow.examples.add(model)
        await uow.commit()

    async with sql_uow as uow:
        entity = await uow.examples.get_by_id(model.id)
        await entity.items.load()
        entity.name = "Item Vlad"
        entity.items.pop()
        entity.items.append(
            ExampleItem(
                name="Item B",
                addresses=alist([
                    Address(city="lersk")
                ])
            )
        )
        entity.items.append(ExampleItem(name="Item C"))

        await entity.items[0].addresses.load()

        entity.items[0].addresses.pop(0)
        entity.items[0].addresses.append(Address(city="Vladivostok"))
        entity.items[0].addresses.append(Address(city="Vladivostok 2"))
        entity.items[0].addresses[0].city = "Lerok"  # changes didn't persist

        await uow.commit()

    async with sql_uow as uow:
        entity = await uow.examples.get_by_id(model.id)
        assert entity.name == "Item Vlad"
        await entity.items.load()
        await entity.items[0].addresses.load()
        await entity.items[1].addresses.load()
        assert len(entity.items) == 3
        assert entity.items[0].addresses[0].city == "Lerok"
        assert entity.items[0].addresses[1].city == "Vladivostok 2"
        assert entity.items[1].addresses[0].city == "lersk"


@pytest.mark.unit
async def test_mem_repo_and_mapper_can_update(
    mem_uow: ITestUnitOfWork
) -> None:
    await test_repo_and_mapper_can_update(mem_uow)
