import pytest
from dataclasses import dataclass

from seedwork.domain.async_structs import alist


@dataclass
class User:
    id: int
    items: alist[int]


@pytest.mark.integration
async def test_can_return_coro_result() -> None:
    user = User(id=1, items=alist([10, 20, 30]))
    assert [10, 20, 30] == await user.items.load()


@pytest.mark.integration
async def test_can_append_value() -> None:
    user = User(id=1, items=alist([10, 20, 30]))
    await user.items.load()
    user.items.append(100)
    assert user.items == [10, 20, 30, 100]


@pytest.mark.integration
async def test_can_compare() -> None:
    user = User(id=1, items=alist([10, 20, 30]))
    await user.items.load()
    assert user.items == [10, 20, 30]


@pytest.mark.integration
async def test_cannot_append_value_to_unloaded_list() -> None:
    user = User(id=1, items=alist([10, 20, 30]))
    with pytest.raises(AssertionError):
        user.items.append(100_000)
