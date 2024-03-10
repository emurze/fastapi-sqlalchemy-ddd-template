# import pytest
# import sqlalchemy
#
# from auth.domain import IAuthUnitOfWork
#
#
# @pytest.mark.integration
# async def test_client_unique_username(uow: IAuthUnitOfWork) -> None:
#     vlad_data = {"username": "vlad"}
#
#     async with uow:
#         await uow.clients.add(**vlad_data)
#         await uow.commit()
#
#     async with uow:
#         with pytest.raises(sqlalchemy.exc.IntegrityError):
#             await uow.clients.add(**vlad_data)
#
#
# @pytest.mark.integration
# async def test_client_username_is_more_than_or_equal_3_characters_error(
#     uow: IAuthUnitOfWork,
# ) -> None:
#     vlad_data = {"username": "vl"}
#     async with uow:
#         with pytest.raises(sqlalchemy.exc.IntegrityError):
#             await uow.clients.add(**vlad_data)
#
#
# @pytest.mark.integration
# async def test_client_username_is_more_than_or_equal_3_characters_success(
#     uow: IAuthUnitOfWork,
# ) -> None:
#     vlad_data = {"username": "vld"}
#     async with uow:
#         await uow.clients.add(**vlad_data)
import pytest

from post.application.command import CreatePostCommand
from post.application.query.get_post import GetPostQuery


@pytest.mark.integration
async def test_bus(memory_bus) -> None:
    command = CreatePostCommand(title='Post', content='Content')
    created_post = await memory_bus.handle_command(command)
    assert created_post.id == 1

    query = GetPostQuery(id=created_post.id)
    post = await memory_bus.handle_query(query)
    assert post.id == 1
    assert post.title == 'Post'
    assert post.content == 'Content'
