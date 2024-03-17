# Add imports

```python
import os
import sys


def add_absolute_imports() -> None:
    """
    It should be called before packages with absolute imports
    """

    sys.path.insert(1, os.path.join(sys.path[0], '..'))
```

# Inject

```python
import functools
import inspect
from collections.abc import AsyncIterator, Callable
from contextlib import asynccontextmanager, suppress
from typing import AsyncGenerator, Any


async def _open_kw_gens(kw: dict) -> tuple[dict, list[AsyncGenerator]]:
    gens = []
    flat_kw = {}

    for key, value in kw.items():
        if inspect.isasyncgenfunction(value):
            async_gen = value()
            flat_kw[key] = await anext(async_gen)
            gens.append(async_gen)
        else:
            flat_kw[key] = value

    return flat_kw, gens


async def _close_gens(gens: list[AsyncGenerator]) -> None:
    for gen in gens:
        with suppress(StopAsyncIteration):
            await anext(gen)


@asynccontextmanager
async def iterate_kw_gens(kw: dict) -> AsyncIterator[dict]:
    flat_kw, gens = await _open_kw_gens(kw)
    yield flat_kw
    await _close_gens(gens)


def inject(**injected_kw) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def inner(*args, **kwargs) -> Any:
            async with iterate_kw_gens(injected_kw) as flat_kw:
                res = await func(*args, **flat_kw, **kwargs)

            return res

        return inner

    return wrapper
```

# Config

```python
import abc
from dataclasses import dataclass
from typing import Protocol

from pydantic import SecretStr, PositiveInt, PostgresDsn
from pydantic_settings import BaseSettings


class WebAPIConfig(Protocol):
    project_title: str
    secret_key: SecretStr


class DatabaseConfig(Protocol):
    db_name: str
    db_user: str
    db_pass: SecretStr
    db_host: str
    db_port: int

    @abc.abstractmethod
    def get_dsn(self, webapi: WebAPIConfig, driver: str) -> str:
        ...


class FastAPIConfig(BaseSettings):
    project_title: str
    secret_key: SecretStr


def get_webapi() -> WebAPIConfig:
    return FastAPIConfig()


class PostgresConfig(BaseSettings):
    db_name: str
    db_user: str
    db_pass: SecretStr
    db_host: str
    db_port: PositiveInt

    def get_dsn(
            self,
            webapi: WebAPIConfig = get_webapi(),
            driver: str = "postgresql+asyncpg",
    ) -> str:
        return str(
            PostgresDsn.build(
                scheme=driver,
                username=self.db_user,
                password=self.db_pass.get_secret_value(),
                host=f"{webapi.project_title}.{self.db_host}",
                port=self.db_port,
                path=self.db_name,
            )
        )


@dataclass(frozen=True, slots=True)
class BaseConfig:
    db: DatabaseConfig
    webapi: WebAPIConfig


config = BaseConfig(
    db=PostgresConfig(),
    webapi=get_webapi(),
)
```

```python
Behavior pattern, return next(gen)
```
