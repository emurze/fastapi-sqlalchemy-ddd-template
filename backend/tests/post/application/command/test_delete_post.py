# import pytest
#
# from post.application.command import CreatePostCommand
# from post.application.command.delete_post import DeletePostCommand
# from post.application.query.get_post import GetPostQuery
# from shared.application.dtos import FailedOutputDto
# from shared.application.messagebus import MessageBus
#
#
# @pytest.mark.unit
# async def test_can_delete_post(bus: MessageBus) -> None:
#     # Given post
#     query = CreatePostCommand(title="Vlad", content="Content")
#     create_output_dto = await bus.handle(query)
#     assert create_output_dto.status
#
#     # When delete post
#     command = DeletePostCommand(id=1)
#     delete_output_dto = await bus.handle(command)
#     assert delete_output_dto.status
#
#     # Then post is not found
#     query = GetPostQuery(id=1)
#     output_dto = await bus.handle(query)
#     assert not output_dto.status
#     assert output_dto.message == FailedOutputDto.RESOURCE_NOT_FOUND_ERROR
#
#
# @pytest.mark.unit
# async def test_delete_post_even_when_no_post(bus: MessageBus) -> None:
#     # Given nothing
#     # When delete post
#     # Then no error
#     command = DeletePostCommand(id=1)
#     output_dto = await bus.handle(command)
#     assert output_dto.status
