import pytest
import sqlalchemy as sa

from shared.infra.database import Model


class Post(Model):
    __tablename__ = 'post'
    id = sa.Column(sa.BIGINT, primary_key=True)
    title = sa.Column(sa.String(256))


@pytest.mark.unit
def test_get_fields_success() -> None:
    assert [*Post.get_fields()] == ['id', "title"]


@pytest.mark.unit
def test_as_dict() -> None:
    post = Post(id=1, title="Post 1")
    assert post.as_dict() == {"id": 1, "title": "Post 1"}
