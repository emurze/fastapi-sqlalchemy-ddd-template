from seedwork.presentation.json_dtos import Schema


class RegisterAccountRequest(Schema):
    name: str


class RegisterAccountResponse(Schema):
    id: int
