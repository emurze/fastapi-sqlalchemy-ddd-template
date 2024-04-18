import pytest

from seedwork.application.messagebus import MessageBus
from tests.conftest import sqlalchemy_container
from tests.seedwork.confdata.containers import get_memory_container


@pytest.fixture(scope="function")
def sql_bus(_restart_example_table) -> MessageBus:
    return sqlalchemy_container.message_bus()


@pytest.fixture(scope="function")
def mem_bus() -> MessageBus:
    """Provides behavior only for simple use cases."""
    memory_container = get_memory_container()
    return memory_container.message_bus()
