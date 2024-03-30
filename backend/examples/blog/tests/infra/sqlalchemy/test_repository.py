import pytest

from blog.domain.entitites import Post
from blog.domain.repositories import IPostRepository


# @pytest.mark.integration
# async def test_add(repo: IPostRepository) -> None:
#     entity_id = await repo.add(Post(title="Hello", content="world", author=1))
#     assert entity_id == 1
#
#
# @pytest.mark.integration
# async def test_add_independence(repo: IPostRepository) -> None:
#     entity_id = await repo.add(Post(title="Hello", content="world", author=))
#     assert entity_id == 1
