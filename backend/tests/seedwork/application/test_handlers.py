import pytest

from seedwork.application.messagebus import MessageBus
from seedwork.domain.errors import ErrorType
from seedwork.domain.services import next_id
from tests.seedwork.confdata.application.command import (
    CreateExampleCommand,
    ExampleItemDTO,
    UpdateExampleCommand,
    DeleteExampleCommand,
)
from tests.seedwork.confdata.application.query import GetExampleQuery
from tests.seedwork.confdata.domain.value_objects import ExampleId


async def create_example(bus: MessageBus) -> ExampleId:
    command = CreateExampleCommand(
        id=next_id(),
        name="Example",
        items=[ExampleItemDTO(id=next_id(), name='Hello')],
    )
    res = await bus.handle(command)
    assert res.is_success()
    return res.payload["id"]


@pytest.mark.unit
async def test_create_example(sql_bus: MessageBus) -> None:
    example_id = await create_example(sql_bus)
    res = await sql_bus.handle(GetExampleQuery(id=example_id))
    assert res.is_success()
    assert res.payload["id"] == example_id
    assert res.payload["name"] == "Example"
    assert res.payload["items"][0]["name"] == 'Hello'


# @pytest.mark.unit
# async def test_update_example(sql_bus: MessageBus) -> None:
#     example_id = await create_example(sql_bus)
#
#     command = UpdateExampleCommand(
#         id=example_id,
#         name="NExample",
#         items=[ExampleItemDTO(id=next_id(), name='NHello')],
#     )
#     res = await sql_bus.handle(command)
#     assert res.is_success()
#
#     res = await sql_bus.handle(GetExampleQuery(id=example_id))
#     assert res.is_success()
#     assert res.payload["id"] == example_id
#     assert res.payload["name"] == "NExample"
#     assert res.payload["items"][0].name == 'NHello'

#
# @pytest.mark.unit
# async def test_delete_example(sql_bus: MessageBus) -> None:
#     example_id = await create_example(sql_bus)
#
#     command = DeleteExampleCommand(id=example_id)
#     res = await sql_bus.handle(command)
#     assert res.is_success()
#
#     res = await sql_bus.handle(GetExampleQuery(id=example_id))
#     assert res.error.type == ErrorType.NOT_FOUND
#
