# import pytest
#
# from post.application.command import CreatePostCommand
# from post.application.command.update_post import UpdatePostCommand
# from post.application.query.get_post import GetPostQuery
# from shared.application.messagebus import MessageBus
#
#
# @pytest.mark.unit
# async def test_can_update_client(bus: MessageBus) -> None:
#     # Given post
#     query = CreatePostCommand(title="Vlad", content="Content")
#     create_output_dto = await bus.handle(query)
#     assert create_output_dto.status
#
#     # When update post
#     command = UpdatePostCommand(id=1, title="Vlad", content="no content")
#     update_output_dto = await bus.handle(command)
#     assert update_output_dto.status
#
#     # Then post is updated
#     query = GetPostQuery(id=1)
#     output_dto = await bus.handle(query)
#     assert output_dto.status
#     assert output_dto.id == 1
#     assert output_dto.title == "Vlad"
#     assert output_dto.content == "no content"
