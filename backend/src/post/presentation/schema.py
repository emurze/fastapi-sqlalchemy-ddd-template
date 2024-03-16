from shared.presentation.json_dtos import Schema


class CreatePostJsonRequest(Schema):
    title: str
    content: str
    draft: bool = False


class CreatePostJsonResponse(Schema):
    id: int


class PostResponse(Schema):
    id: int
    title: str
    content: str
    draft: bool = False
