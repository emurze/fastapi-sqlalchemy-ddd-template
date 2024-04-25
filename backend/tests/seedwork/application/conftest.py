import pytest

from seedwork.application.messagebus import MessageBus
from tests.seedwork.confdata.container import containers


@pytest.fixture(scope="function")
def sql_bus(_restart_example_table) -> MessageBus:
    return containers.sql_container.message_bus()


@pytest.fixture(scope="function")
def mem_bus() -> MessageBus:
    """Provides behavior only for simple use cases."""
    memory_container = containers.get_memory_container()
    return memory_container.message_bus()
