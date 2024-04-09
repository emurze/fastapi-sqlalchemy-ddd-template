import pytest
from dataclasses import dataclass

from seedwork.domain.collection import alist


async def coro():
    return [10, 20, 30]


@dataclass
class User:
    id: int
    items: alist

    async def find(self, value: int) -> bool:
        for item in await self.items.as_async:
            if item == value:
                return True
        return False

    def add_item(self, value: int) -> None:
        self.items.append(value)


@pytest.mark.integration
async def test_can_return_coro_result() -> None:
    user = User(id=1, items=alist(coro=coro))
    res = await user.items.as_async
    assert res == [10, 20, 30]


@pytest.mark.integration
async def test_can_find() -> None:
    user = User(id=1, items=alist(coro=coro))
    res = await user.find(20)
    assert res is True


@pytest.mark.integration
async def test_can_append() -> None:
    user = User(id=1, items=alist(coro=coro))
    user.add_item(1)
    assert user.items == [1]
