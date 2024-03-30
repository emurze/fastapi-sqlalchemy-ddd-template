from collections.abc import Callable
import time
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel


def check(func: Callable) -> Callable:
    def wrapper(*args, **kw) -> Any:
        t0 = time.perf_counter()
        res = func(*args, **kw)
        print(f"time - {time.perf_counter() - t0}")
        return res
    return wrapper


class PydanticAccount(BaseModel):
    id: int
    name: str


@check
def run_pydantic_basemodel(quantity: int = 1_000_000) -> None:
    for number in range(quantity):
        account = PydanticAccount(id=number, name="account")
        assert account.id == number
        assert account.name == "account"


@dataclass(frozen=True, slots=True)
class DataclassAccount:
    id: int
    name: str


@check
def run_python_dataclass(quantity: int = 1_000_000) -> None:
    for number in range(quantity):
        account = DataclassAccount(id=number, name="account")
        assert account.id == number
        assert account.name == "account"


if __name__ == '__main__':
    run_python_dataclass()
    run_pydantic_basemodel()
