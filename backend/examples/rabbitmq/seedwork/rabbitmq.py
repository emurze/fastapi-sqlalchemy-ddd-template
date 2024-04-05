from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

import pika
from pika.adapters.blocking_connection import BlockingChannel


@dataclass(frozen=True, slots=True)
class RabbitConnection:
    host: str
    port: int
    user: str
    password: str
    encoding: str = 'utf-8'

    @contextmanager
    def connect(self) -> Iterator[BlockingChannel]:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=self.host,
                port=self.port,
                credentials=pika.PlainCredentials(
                    username=self.user,
                    password=self.password,
                ),
            )
        )
        yield connection.channel()
        connection.close()
