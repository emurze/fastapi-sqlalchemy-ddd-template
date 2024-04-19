import pytest

from seedwork.application.messagebus import MessageBus
from tests.seedwork.confdata.domain import ExampleId
from tests.seedwork.confdata.handlers.command import (
    CreateExampleCommand,
    ExampleItemDTO,
    UpdateExampleCommand,
)
from tests.seedwork.confdata.handlers.query import GetExampleQuery


async def create_example(bus: MessageBus) -> ExampleId:
    command = CreateExampleCommand(
        name="Example",
        items=[ExampleItemDTO(name='Hello')],
    )
    res = await bus.handle(command)
    assert not res.error
    return res.payload["id"]


@pytest.mark.unit
async def test_create_example(mem_bus: MessageBus) -> None:
    example_id = await create_example(mem_bus)
    query = GetExampleQuery(id=example_id)
    res = await mem_bus.handle(query)
    assert res.payload["id"] == example_id
    assert res.payload["name"] == "Example"
    assert res.payload["items"][0].name == 'Hello'


@pytest.mark.unit
async def test_update_example(mem_bus: MessageBus) -> None:
    example_id = await create_example(mem_bus)
    assert example_id

    command = UpdateExampleCommand(
        id=example_id,
        name="Example",
        items=[ExampleItemDTO(name='Hello')],
    )
    await mem_bus.handle(command)
