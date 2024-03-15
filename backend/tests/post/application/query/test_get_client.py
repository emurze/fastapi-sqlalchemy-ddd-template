import pytest

from post.application.command import CreatePostCommand
from post.application.query.get_post import GetPostQuery
from shared.application.dtos import FailedOutputDto
from shared.application.messagebus import MessageBus


@pytest.mark.unit
async def test_can_get_post(bus: MessageBus) -> None:
    # Given post
    query = CreatePostCommand(title="Vlad", content="Content")
    create_output_dto = await bus.handle(query)
    assert create_output_dto.status

    # When get post
    # Then post is retrieved
    query = GetPostQuery(id=1)
    output_dto = await bus.handle(query)
    assert output_dto.status
    assert output_dto.id == 1


@pytest.mark.unit
async def test_get_post_not_found_error(bus: MessageBus) -> None:
    # Given nothing
    # When get post
    # then not found error
    query = GetPostQuery(id=1)
    output_dto = await bus.handle(query)
    assert not output_dto.status
    assert output_dto.message == FailedOutputDto.RESOURCE_NOT_FOUND_ERROR
