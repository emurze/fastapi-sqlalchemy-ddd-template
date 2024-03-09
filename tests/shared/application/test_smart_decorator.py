from collections.abc import Awaitable, Callable
from typing import TypeVar

from pydantic import BaseModel

from shared.application.queries import QueryResult, QueryPayload

T = TypeVar("T")


class User(BaseModel):
    id: int
    name: str


def handler_query(response_model):
    def wrapper(func: Callable):
        async def inner(*args, **kw) -> Awaitable[T]:
            res = await func(*args, **kw)
            # func.__annotations__['return'] = response_model
            return res

        return inner

    return wrapper


class UserQueryPayload(QueryPayload):
    id: int
    name: str


class GetUserResult(QueryResult):
    pass


def get_client() -> int:
    payload = UserQueryPayload(id=1, name="Vlad")
    return GetUserResult(payload=payload)


async def test_deco():
    res = get_client()
    print(res)
