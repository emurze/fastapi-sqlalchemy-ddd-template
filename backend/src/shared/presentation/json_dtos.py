from pydantic import BaseModel, ConfigDict
from starlette import status

from shared.domain.errors import Error


class Schema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class FailedJsonResponse(Schema):
    detail: str


STATUS_CODES = {
    Error.NOT_FOUND: status.HTTP_404_NOT_FOUND,
    Error.CONFLICT: status.HTTP_409_CONFLICT,
    Error.VALIDATION: status.HTTP_400_BAD_REQUEST,  # or param error
    Error.UNAUTHORIZED: status.HTTP_401_UNAUTHORIZED,
    Error.SYSTEM: status.HTTP_500_INTERNAL_SERVER_ERROR,
}
