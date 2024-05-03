from uuid import UUID

import pytest

from seedwork.application.messagebus import MessageBus
from seedwork.domain.services import next_id
from tests.seedwork.confdata.application import command
from tests.seedwork.confdata.application.command import DeleteExampleCommand, \
    DeleteExampleItemCommand
from tests.seedwork.confdata.application.query import GetExampleQuery, \
    GetExampleItemQuery


async def create_example(bus: MessageBus) -> tuple[UUID, UUID]:
    item_id = next_id()
    cmd = command.CreateExampleCommand(
        id=next_id(),
        name="Example",
        items=[command.ExampleItemDTO(id=item_id, name="Hello")],
    )
    res = await bus.handle(cmd)
    assert res.is_success()
    return cmd.id, item_id


@pytest.mark.unit
async def test_create_example(sql_bus) -> None:
    example_id, _ = await create_example(sql_bus)
    result = await sql_bus.handle(GetExampleQuery(id=example_id))
    assert result.is_success()
    assert result.payload["id"] == example_id
    assert result.payload["name"] == "Example"
    assert result.payload["items"][0]["name"] == "Hello"


@pytest.mark.unit
async def test_update_example(sql_bus) -> None:
    example_id, item_id = await create_example(sql_bus)
    res = await sql_bus.handle(
        command.UpdateExampleCommand(id=example_id, name="Hello")
    )
    assert res.is_success()

    res = await sql_bus.handle(
        command.UpdateExampleItemCommand(
            example_id=example_id,
            item_id=item_id,
            name="New Item",
        )
    )
    assert res.is_success()

    res = await sql_bus.handle(GetExampleQuery(id=example_id))
    assert res.is_success()
    assert res.payload["name"] == "Hello"
    assert res.payload["items"][0]["name"] == "New Item"


@pytest.mark.unit
async def test_delete_example(sql_bus) -> None:
    example_id, _ = await create_example(sql_bus)
    await sql_bus.handle(DeleteExampleCommand(id=example_id))
    assert (await sql_bus.handle(GetExampleQuery(id=example_id))).is_failure()


@pytest.mark.unit
async def test_delete_example_item(sql_bus) -> None:
    example_id, item_id = await create_example(sql_bus)
    await sql_bus.handle(
        DeleteExampleItemCommand(example_id=example_id, item_id=item_id)
    )
    res = await sql_bus.handle(GetExampleItemQuery(id=example_id))
    assert res.is_failure()


# todo: DDD how to update relations
# todo: new more difficult test with domain events\
# todo: integration
