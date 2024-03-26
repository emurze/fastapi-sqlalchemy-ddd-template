import pytest
from pydantic import ValidationError

from blog.domain.entitites import Post


@pytest.mark.unit
def test_validation() -> None:
    title = "lerka" * 100
    with pytest.raises(ValidationError):
        Post(title=title, content="content")
