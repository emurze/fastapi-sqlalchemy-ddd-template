import pytest

from post.application.command import CreatePostCommand
from post.application.query.get_post import GetPostQuery
from shared.application.messagebus import MessageBus


@pytest.mark.unit
async def test_can_create_post(bus: MessageBus) -> None:
    # Given nothing
    # When create post
    query = CreatePostCommand(title="Vlad", content="Content")
    output_dto = await bus.handle(query)
    assert output_dto.status
    assert output_dto.id == 1

    # Then post is created
    query = GetPostQuery(id=1)
    output_dto = await bus.handle(query)
    assert output_dto.status
    assert output_dto.title == "Vlad"
    assert output_dto.content == "Content"
