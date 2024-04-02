import asyncio

import pytest

from auth.application.command.register_account import RegisterAccountCommand


@pytest.mark.integration
async def test_concurrent_regs_are_allowed(sqlalchemy_bus) -> None:
    command = RegisterAccountCommand(name="account 1")
    await asyncio.gather(
        *[sqlalchemy_bus.handle(command) for _ in range(50)],
    )
