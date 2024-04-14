import pytest

from seedwork.domain.async_structs import alist
from seedwork.domain.services import next_id
from tests.seedwork.confdata.domain import Example, ExampleItem, Address
from tests.seedwork.confdata.repositories import (
    ExampleMapper,
    ExampleModel,
    ExampleItemModel,
    AddressModel,
)


class TestExampleMapper:
    mapper = ExampleMapper()

    @pytest.mark.unit
    async def test_model_to_entity(self) -> None:
        example = ExampleModel(
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
        entity = self.mapper.model_to_entity(example)
        await entity.items.load()
        await entity.items[0].addresses.load()
        assert entity.name == 'Example1'
        assert entity.items[0].name == 'ExampleItem1'
        assert entity.items[0].addresses[0].city == 'Kiev'

    @pytest.mark.unit
    def test_entity_to_model(self) -> None:
        example = Example(
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
        model = self.mapper.entity_to_model(example)
        assert model.name == 'Example1'
        assert model.items[0].name == 'ExampleItem1'
        assert model.items[0].addresses[0].city == 'Kiev'

    @pytest.mark.unit
    async def test_entity_to_model_then_model_to_entity(self) -> None:
        example = ExampleModel(
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
        entity = self.mapper.model_to_entity(example)
        await entity.items.load()
        await entity.items[0].addresses.load()

        model = self.mapper.entity_to_model(entity)
        assert model.name == 'Example1'
        assert model.items[0].name == 'ExampleItem1'
        assert model.items[0].addresses[0].city == 'Kiev'
