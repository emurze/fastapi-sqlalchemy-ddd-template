import asyncio

from pika.adapters.blocking_connection import BlockingChannel

from container import container
from examples.rabbitmq.seedwork.rabbitmq import RabbitConnection


def callback(channel: BlockingChannel, method, properties, body) -> None:
    print(f"{body=}")


async def main(conn: RabbitConnection) -> None:
    with conn.connect() as channel:
        channel.queue_declare(queue="queue1")
        channel.basic_publish(
            exchange="",
            routing_key="queue1",
            body=b"Hello world!",
        )

    with conn.connect() as channel:
        channel.queue_declare(queue="queue1")
        channel.basic_publish(
            exchange="",
            routing_key="queue1",
            body=b"Hello world!",
        )

    with conn.connect() as channel:
        channel.queue_declare(queue="queue1")
        channel.basic_publish(
            exchange="",
            routing_key="queue1",
            body=b"Hello world!",
        )

    with conn.connect() as channel:
        channel.queue_declare(queue="queue1")
        channel.basic_consume(
            queue="queue1",
            auto_ack=True,
            on_message_callback=callback,
        )
        channel.start_consuming()


if __name__ == '__main__':
    asyncio.run(main(conn=container.rabbitmq_conn()))
