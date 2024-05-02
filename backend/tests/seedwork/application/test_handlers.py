import pytest

from seedwork.application.messagebus import MessageBus
from seedwork.domain.services import next_id
from tests.seedwork.confdata.application.command import (
    CreateExampleCommand,
    ExampleItemDTO,
)
from tests.seedwork.confdata.application.query import GetExampleQuery
from tests.seedwork.confdata.domain.value_objects import ExampleId


async def create_example(bus: MessageBus) -> ExampleId:
    command = CreateExampleCommand(
        id=next_id(),
        name="Example",
        items=[ExampleItemDTO(id=next_id(), name="Hello")],
    )
    res = await bus.handle(command)
    assert res.is_success()
    return res.payload["id"]


# @pytest.mark.marked
# @pytest.mark.unit
# async def test_create_example(sql_bus: MessageBus) -> None:
#     example_id = await create_example(sql_bus)
#     res = await sql_bus.handle(GetExampleQuery(id=example_id))
#     assert res.is_success()
#     assert res.payload["id"] == example_id
#     assert res.payload["name"] == "Example"
#     assert res.payload["items"][0]["name"] == "Hello"
