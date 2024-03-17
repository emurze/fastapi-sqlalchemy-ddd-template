from shared.domain.entities import AggregateRoot
from shared.domain.pydantic_v1 import dataclass, Field


@dataclass(kw_only=True)
class Post(AggregateRoot):
    title: str = Field(max_length=256)
    content: str = Field(max_length=256)
    draft: bool = False


if __name__ == '__main__':
    post = Post(title="lerka", content="content")
    post.update(**{"title": "lerka" * 100})
