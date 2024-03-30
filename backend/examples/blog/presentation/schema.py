from seedwork.presentation.json_dtos import Schema


class CreatePostResponse(Schema):
    id: int


class PostRequest(Schema):
    title: str
    content: str
    draft: bool = False
    author_id: int


class PostResponse(Schema):
    id: int
    title: str
    content: str
    draft: bool = False
    author_id: int
