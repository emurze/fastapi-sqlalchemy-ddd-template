import pytest

from seedwork.application.messagebus import MessageBus
from tests.seedwork.confdata.handlers.command import (
    CreateExampleCommand,
    ExampleItemDTO,
)


@pytest.mark.unit
async def test_create_example(mem_bus: MessageBus) -> None:
    command = CreateExampleCommand(
        name="Example",
        items=[ExampleItemDTO(name='Hello')],
    )
    res = await mem_bus.handle(command)
    assert res.payload["id"]
    # Check it
