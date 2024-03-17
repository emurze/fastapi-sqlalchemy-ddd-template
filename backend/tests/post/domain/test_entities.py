import pytest

from post.domain.entitites import Post
from shared.domain.pydantic_v1 import ValidationError


def test_validation() -> None:
    title = "lerka" * 100
    with pytest.raises(ValidationError):
        Post(title=title, content="content")
