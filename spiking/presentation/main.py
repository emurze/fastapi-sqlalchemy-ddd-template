import asyncio

from seedwork.domain.services import next_id
from spiking.application.create_post import CreatePostCommand, AuthorDTO
from spiking.application.get_post import GetPostQuery
from spiking.infra.database import restart_db
from spiking.infra.tables import start_mappers
from spiking.presentation.container import Container


async def prepare_env(engine) -> None:
    await restart_db(engine)
    start_mappers()


async def main() -> None:
    container = Container()
    await prepare_env(container.engine())

    post_id = next_id()
    bus = container.messagebus()
    await bus.handle(
        CreatePostCommand(
            id=post_id,
            name="Post 1",
            description="New mega post.",
            rate=7,
            draft=True,
            authors=[AuthorDTO(id=next_id(), name="Vlad")]
        )
    )
    result = await bus.handle(GetPostQuery(id=post_id))
    print(f"{result=}")
    assert result.payload["draft"] is False


if __name__ == '__main__':
    asyncio.run(main())
