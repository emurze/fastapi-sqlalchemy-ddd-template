from shared.presentation.json_dtos import Schema


class CreatePostJsonRequest(Schema):
    title: str
    content: str
    draft: bool = False


class CreatePostJsonResponse(Schema):
    id: int
    title: str
    content: str
    draft: bool = False


class GetPostJsonResponse(CreatePostJsonResponse):
    pass


class UpdatePostJsonRequest(CreatePostJsonRequest):
    pass


class UpdatePostJsonResponse(CreatePostJsonResponse):
    pass
