import pytest

from auth.application.command.register_account import RegisterAccountCommand
from seedwork.application.messagebus import MessageBus


@pytest.mark.unit
async def test_register_account_success(bus: MessageBus) -> None:
    command = RegisterAccountCommand(name="account 1")
    result = await bus.handle(command)
    assert result.payload.id == 1
