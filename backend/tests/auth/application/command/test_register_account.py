import pytest

from auth.application.command.register_account import RegisterAccountCommand
from seedwork.application.messagebus import MessageBus


@pytest.mark.skip(reason="Making pubsub event sourcing")
@pytest.mark.unit
async def test_can_register_account(bus: MessageBus) -> None:
    command = RegisterAccountCommand(name="account 1")
    result = await bus.handle(command)
    assert result.payload.id == 1


@pytest.mark.skip(reason="Making pubsub event sourcing")
@pytest.mark.unit
async def test_concurrent_registrations_are_allowed(bus: MessageBus) -> None:
    pass
