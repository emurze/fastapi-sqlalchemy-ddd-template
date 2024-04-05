from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton

from examples.rabbitmq import config
from examples.rabbitmq.seedwork.rabbitmq import RabbitConnection


def get_conn() -> RabbitConnection:
    return RabbitConnection(
        host=config.RABBITMQ_HOST,
        port=config.RABBITMQ_PORT,
        user=config.RABBITMQ_USER,
        password=config.RABBITMQ_PASS,
    )


class Container(DeclarativeContainer):
    rabbitmq_conn: RabbitConnection = Singleton(get_conn)


container = Container()
